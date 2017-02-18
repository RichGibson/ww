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
from ww.models import Word, Source, SourceType, WordSource, Sentence, WordSentence


import enchant
d=enchant.Dict('de_DE')

def clean_line(line):

    #if re.search('[a..zA..Z]', line):
    #    line = line
    #else:
    #    line = ''

    line=re.sub('\.','',line)
    line=re.sub('"','',line)
    line=re.sub("!",'',line)
    line=re.sub("'",'',line)
    line=re.sub('\(','',line)
    line=re.sub('\)','',line)
    line=re.sub(',','',line)
    line=re.sub('\?','',line)
    line=re.sub('-','',line)
    line=re.sub('”','',line)
    line=re.sub('“','',line)
    line=re.sub('„','',line)
    line=re.sub('…','',line)
    line=re.sub('\|',' ',line)
    #line= line.lower()

    return line

def saveWords(words):
    """
    """
    w = Word()
    w.word = word
    w.save()
    ws = WordSource()
    ws.source = s
    ws.word = w
    ws.save()

def isWord(word):
    """
    is this a word?
    """
    #todo: this doesn't work, mögen doesn't fucking match.

    flag = False
    # do we have any (non special) letters?
    if re.search('[A..Za..z]',word, re.UNICODE):
        flag=True
       
    # does enchant think it is a word? This doesn't work for names...
    # so maybe it is the right thing?
    if d.check(word):
        flag=True

    if re.match("([\d]+)$", word):
        flag=False

    if not flag:
        #i = codecs.open(file, 'r', 'latin-1')
        #lines = f.readlines()
        print "not a word? ", word
        #pdb.set_trace()

    return flag

def XloadWordFile(file):
    """
    Reads a file and loads it into the Word model
    """
    cnt = 0

    print "loadWordFile: ", file

    # lives of others is latin-1, other files are utf-8.
    try:
        f = codecs.open(file, 'r', 'utf-8')
        lines = f.readlines()
    except:
        print "utf-8 failed"
        f = codecs.open(file, 'r', 'latin-1')
        lines = f.readlines()

    #f = codecs.open(file, 'r', 'latin-1')
    #lines = f.readlines()

    print "do we have lines?", lines
    # this worked for a lot of files
    #f = codecs.open(file, 'r', 'utf-8')
    #f = codecs.open(file, 'r', 'ISO-8859-1')

    s=Source()
    s.fulltext="".join(lines)
    s.notes = "imported by data_word.py"
    s.name=file
    s.save()

    #words = set()
    words = {}
    for line in lines:
        if len(line) > 0:
            #print "    line: ", line
            print "line start: ", line
            line = clean_line(line)
            print "line clean: ", line
            pass

        if len(line) > 0:
            for word in line.split():
                #print "--"
                #print type(word)
                #print "(raw) word: %r " % (word)
                #print "(%% s) word: %s " % (word)
                #print "unicode_escape : ", word.encode("unicode_escape")
                #print "encode utf-8: ", word.encode("utf-8")

                if not isWord(word):
                    continue

                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

        cnt+=1
    f.close()

    print "adding words"
    print words.keys()
    for word in words.keys():
        print "adding ", word
        w = Word.objects.filter(word=word)
        if len(w)>0:
            w = w[0]
        else:
            w=Word()
        w.word = word
        w.save()

        ws = WordSource()
        ws.source = s
        ws.word = w
        ws.cnt = words[word]
        ws.save()

    return words


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

    print "do we have raw?", raw[0:100], "..."

    s=Source()
    s.fulltext="".join(raw)
    s.notes = "imported by data_word.py"
    s.name=file
    s.save()

    lst = pattern.de.parse(raw)
    cnt=1
    word_lst = {}
    for sent in pattern.de.split(lst):
        st=sent.string
        st=re.sub(" ([!?,.])",r'\1',st)

        sentence=Sentence()
        sentence.sentence=st
        sentence.save()
        words = sent.string.split()
        print sentence
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
            wsent.sentence = sentence
            wsent.word = w
            wsent.save()

            cnt+=1

    for word in word_lst:
        ws = WordSource()
        ws.source = s
        ws.word = word_lst[word]['id']
        ws.cnt = word_lst[word]['cnt']
        ws.save()


    f.close()
    return

    return words


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

####################################

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
    #print "-" * 40
    #print "Loading file: ", file
    words=loadWordFile(file)


print "-" * 40
print "all done"




# do something with a concordance :-/

import codecs

# I've lost my umlauts. 
#f=codecs.open(infile, 'r', 'ISO-8859-1')
#f=codecs.open(infile, 'r', 'windows-1252')
        
#words_sorted = sorted(words.iteritems(), key=operator.itemgetter(1))



