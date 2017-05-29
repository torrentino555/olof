from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404
from questions.models import Question, Answer, Profile, Tag, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from questions.forms import LoginForm, CommentForm, AskForm, SettingsForm, RegistrationForm

def init(request, title):
    context = {}
    context.update(csrf(request))
    context['title'] = title
    context['tags'] = Tag.objects.all().order_by('-count')[:3]
    context['members'] = Profile.objects.all()[:4]
    if request.user.is_authenticated:
        context['user'] = Profile.objects.get(user=request.user)
    return context

def index(request):
    context = init( request, 'Questions')
    return pag(request, Question.objects.new_questions(), 'questions', 'index.html', context)

def hot(request):
    context = init( request, 'Hot')
    return pag(request, Question.objects.hot_questions(), 'questions', 'hot.html', context)

def tag(request, tag_name):
    context = init( request, 'Tag:' + tag_name)
    context['tag'] = tag_name
    tag = Tag.objects.get(name__exact=tag_name)
    quest = Question.objects.all()
    questions = []
    for q in quest:
        for t in q.tags.all():
            if t == tag:
                questions.append(q)
    return pag(request, questions, 'questions', 'tag.html', context)

def question(request, id):
    q = get_object_or_404(Question, pk=id)
    context = init( request, q.title)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(context['user'], q)
            return HttpResponseRedirect(reverse('question', args=[id]))
    else:
        context['question'] = q
        context['comments'] = Answer.objects.filter(question=q)
        context['form'] = CommentForm()
    return render(request, 'question.html', context)

def log_in(request):
    context = init( request, 'Login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            f = form.auth()
            login(request, f)
            return HttpResponseRedirect(request.GET['continue'])
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(request.GET['continue'])

def signup(request):
    context = init( request, 'Registration')
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'signup.html', context)

@login_required
def ask(request):
    context = init( request, 'Ask')
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            id = form.save(context['user'])
            print(request.POST['tags'])
            return HttpResponseRedirect(reverse('question', args=[id]))
    else:
        context['form'] = AskForm()
    return render(request, 'ask.html', context)

@login_required
def settings(request):
    context = init( request, 'Settings')
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(context['user'])
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SettingsForm(initial={'login':context['user'].user.username, 'email':context['user'].user.email, 'username':context['user'].username, 'avatar':context['user'].avatar})
    context['form'] = form
    return render(request, 'settings.html', context)

def pag(request, objects, name_objects, name_html, kwargs):
    paginator = Paginator(objects, 4)
    page = request.GET.get('page')

    page_obj = {}
    try:
        page_obj = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        page = 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    kwargs[name_objects] = page_obj
    kwargs['page_cur'] = page
    kwargs['page_last'] = paginator.num_pages
    if paginator.num_pages > 1:
        kwargs['pag'] = True
    if paginator.num_pages > 2:
        if page == 1:
            kwargs['pag_numbers'] = ['1', '2', '3']
        elif page == paginator.num_pages:
            kwargs['pag_numbers'] = [str(page - 2), str(page - 1), str(page)]
        else:
            kwargs['pag_numbers'] = [str(page - 1), str(page), str(page + 1)]
    else:
        kwargs['pag_numbers'] = []
        for i in range(1, paginator.num_pages + 1):
            kwargs['pag_numbers'].append(str(i))
    return render(request, name_html, kwargs)
