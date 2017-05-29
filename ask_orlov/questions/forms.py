from django.forms import ModelForm, Form
from django import forms
from .models import Question, Profile, Answer, Tag
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Password')
    __user = None

    def clean(self):
        try:
            self.__user = auth.authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
        except:
            raise forms.ValidationError('Invaild login or password')

    def auth(self):
        if not self.__user:
            self.clean()
        return self.__user

class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def save(self, user):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        question.author = user
        question.save()
        return question.id

class RegistrationForm(Form):
    login = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(label='NickName',max_length=50)
    password = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat Password')
    avatar = forms.ImageField(label='Upload avatar')

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Password mismatching')

    def save(self):
        user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'], self.cleaned_data['password'])
        user.save()
        profile = Profile(user=user, username=self.cleaned_data['username'], avatar=self.cleaned_data['avatar'])
        profile.save()
        return profile

class SettingsForm(Form):
    login = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    avatar = forms.ImageField(label='Upload avatar')

    def save(self, user):
        user.user.username = self.cleaned_data['login']
        user.user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.avatar = self.cleaned_data['avatar']
        user.user.save()
        user.save()
        return user

class CommentForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, user, question):
        comment = Answer(text=self.cleaned_data['text'], author=user, question=question)
        question.count_answers += 1
        question.save()
        comment.save()
        return comment
