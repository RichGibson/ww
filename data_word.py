##### -*- coding: utf-8 -*-
#!/usr/bin/env python

# data_word.py - load some word data

# to run:
# docker-compose run web python data_word.py
import os, sys, re
import csv
import django
import pdb
import string
import pattern.de


import codecs
import operator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ww.settings")
django.setup()

from django.conf import settings
from ww.models import Word, Source, SourceType, WordSource, Sentence, WordSentence, UserWord
import ww.views

from django.contrib.auth.models import User 

import enchant
d=enchant.Dict('de_DE')

def loadWordText(raw, source_name, user):
    """
    take a text, add it...
    """
    S=Source()
    S.fulltext="".join(raw)
    S.notes = "imported by data_word.py"
    S.name=source_name
    S.save()

    lst = pattern.de.parse(raw)
    cnt=1
    word_lst = {}
    for sent in pattern.de.split(lst):
        st=sent.string
        st=re.sub(" ([!?,.])",r'\1',st)

        SENTENCE=Sentence()
        SENTENCE.sentence=st
        SENTENCE.source=S
        SENTENCE.save()

        words = sent.string.split()
        for word in words:
            print "\tadding word ", word
            # is this a word?
            word = word.strip(string.punctuation)
            if len(word) == 0:
                continue
            w = Word.objects.filter(word=word)
            if len(w)>0:
                w = w[0]
            else:
                w=Word()
                w.word = word
                w.save()

            if word in word_lst:
                word_lst[word]['cnt'] +=1
            else:
                word_lst[word] = {'id':w, 'cnt':1}

            wsent = WordSentence()
            wsent.sentence = SENTENCE
            wsent.word = w
            wsent.save()

            uw = UserWord()
            uw.user = user
            uw.word =w
            uw.save()

            cnt+=1

    for word in word_lst:
        ws = WordSource()
        ws.source = S
        ws.word = word_lst[word]['id']
        ws.cnt = word_lst[word]['cnt']
        ws.save()

    return


def loadWordFile(file):
    """
    Reads a file and loads it into the Word model
    """
    cnt = 0
    print "loadWordFile: ", file

    # lives of others is latin-1, other files are utf-8.
    try:
        f = codecs.open(file, 'r', 'utf-8')
        raw = f.read()
    except:
        print "utf-8 failed"
        f = codecs.open(file, 'r', 'latin-1')
        raw = f.read()

    f.close()

    print "do we have raw?", raw[0:100], "..."
    user=User.objects.all()
    user=user[0]
    loadWordText(raw, "file: %s " % file, user)

    return


####################################
# delete

Word.objects.all().delete()
try:
    Word.objects.all().delete()
    Source.objects.all().delete()
    WordSource.objects.all().delete()
    Sentence.objects.all().delete()
    WordSentence.objects.all().delete()
    pass
except:
    print "delete failed!"
    sys.exit(2)
    pass


data_files = [
        #'misc/test.txt',
        #'misc/test_lives.srt',
        #'misc/lives_of_others.srt',
        'misc/kippen.txt',
        'misc/besser_gehts_nicht.txt',
        'misc/99_luftballons.txt',
        'misc/spacewar.txt',
        'misc/sie_mögen_sich.txt',
        'misc/harrypotter.txt',
        #'misc/lola_rentt.txt',
        ]

for file in data_files:
    words=loadWordFile(file)

print "all done"
