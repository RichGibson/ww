from __future__ import unicode_literals
import sys
import re
import pdb
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class UserWord(models.Model):
    user = models.ForeignKey(User)
    #user = models.ForeignKey(settings.auth_user_model)
    word = models.ForeignKey('word')

    def __str__(self):
        return "%s - %s" % (self.user, self.word.word)
        #return "%s - %s" % (self.user, self.word)

class Word(models.Model):
    word = models.CharField(max_length=255, blank=True)
    plural = models.CharField(max_length=255, blank=True)
    article = models.CharField(max_length=3, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.word.encode('utf8')


class WordSentence(models.Model):
    word = models.ForeignKey("word", null=True, )
    sentence = models.ForeignKey("sentence", null=True, )

    def __unicode__(self):
        w = self.word.word
        s = self.sentence.sentence
        return w+": "+s
        #return "%s: %s" % (w.encode('utf-8'),s.encode('utf-8'))

class SourceType(models.Model):
    sourcetype = models.CharField(max_length=25, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sourcetype

class Source(models.Model):
    name = models.CharField(max_length=255, blank=True)
    source_type = models.ForeignKey("sourcetype", null=True, )

    notes = models.TextField(blank=True, null=True)
    fulltext = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name.encode('utf8')

class WordSource(models.Model):
    word = models.ForeignKey("word", null=True, )
    source = models.ForeignKey("source", null=True, )
    cnt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "wordsource"
        #return "%s - %s" % (self.word, self.source.name.encode('utf8'))
 

class Sentence(models.Model):
    sentence = models.TextField(blank=True, null=True)
    source = models.ForeignKey("source", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sentence.encode('utf-8')




