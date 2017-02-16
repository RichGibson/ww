##### -*- coding: utf-8 -*-
#!/usr/bin/env python

# data_word.py - load some word data

# to run:
# docker-compose run web python data_word.py

import os, sys, re
import csv
import django
import pdb

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ww.settings")
django.setup()
import codecs
import operator


from django.conf import settings
from ww.models import Word, Source, SourceType, WordSource

def fixValue(key, val):
    """
    take a value, fix it/reformat whatever needed.
    """

    key = key.lower()
    #print "fixValue key: %s val: %s " % (key, val)

    # remove (None none) only at start of string
    if re.match('none', val, re.IGNORECASE):
        val = ''

    # remove Unknown
    if re.match('unknown', val, re.IGNORECASE):
        val = ''

    # remove N/A NA, only at start of string
    if re.match('^N/?A$', val, re.IGNORECASE):
        val = ''

    # cities that have 'Berkeley, CA'
    m = re.match('Berk', val)
    if m:
        val = "Berkeley"

    if key == 'property_type':
        #outfile.write("%r\n" % val)
        (val,foo) = Property.propertyTypeFromString(val)
        #print "property type for %s = %r" % (key, val)


    return val

def add_words(line, words):
    """ add the words in line to the dict words """ 
    for word in line.split():
        if re.search('ffne', line):
            print "word %s" % (word.encode('ascii','ignore'))
            # sys.exit(2)
        if word in words.keys():
            words[word] = words[word]+1
        else:
            words[word] = 1



def clean_line(line):
    if re.search('[a..zA..Z]', line):
        line = line
    else:
        line = ''
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
    line= line.lower()

    return line


def loadWordFile(file):
    """
    Reads a file and loads it into the Word model
    """
    cnt = 0

    f = codecs.open(file, 'r', 'ISO-8859-1')
    lines = f.readlines()
    s=Source()
    s.fulltext="".join(lines)
    s.notes = "imported by data_word.py"
    s.name=file
    s.save()

    for line in lines:
        print "line", line
        #AddProperty(row, file)
        line = clean_line(line)
        if len(line) > 0:
            for word in line.split():
                if re.search('ffne', line):
                    print "word %s" % (word.encode('ascii','ignore'))
                    # sys.exit(2)
                #print "\t%s : %s " % (file, word)
                print word
                w = Word()
                w.word = word
                w.save()
                ws = WordSource()
                ws.source = s
                ws.word = w
                ws.save()
        cnt+=1
    f.close()


####################################
# delete

try:
    Word.objects.all().delete()
    Source.objects.all().delete()
    pass
except:
    print "delete failed!"
    sys.exit(2)
    pass

####################################

data_files = [
        'misc/besser_gehts_nicht.txt',
        'misc/99_luftballons.txt',
        #'misc/spacewar.txt',
        'misc/sie_mögen_sich.txt',
        ]

for file in data_files:
    print "Loading file: ", file
    loadWordFile(file)

print "-" * 40
print "all done"




# do something with a concordance :-/

import codecs

# I've lost my umlauts. 
#f=codecs.open(infile, 'r', 'ISO-8859-1')
#f=codecs.open(infile, 'r', 'windows-1252')
        
#words_sorted = sorted(words.iteritems(), key=operator.itemgetter(1))



