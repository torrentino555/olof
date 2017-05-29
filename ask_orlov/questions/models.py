# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to="uploads/")
    username = models.CharField(max_length=50)
    def __unicode__(self):
        return u'{}'.format(self.username)

class QuestionManager(models.Manager):
    def hot_questions(self):
        return self.order_by('-rating')
    def new_questions(self):
        return self.order_by('-time_create')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Profile)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    time_create = models.DateTimeField(default=datetime.now)
    tags = models.ManyToManyField('Tag')
    count_answers = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{}'.format(self.title)


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile)
    time_create = models.DateTimeField(default=datetime.now)
    question = models.ForeignKey(Question)
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{}'.format(self.text)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{}'.format(self.name)
