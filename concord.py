##### -*- coding: utf-8 -*-
# do something with a concordance :-/

import codecs
import re
import sys
import operator

infile = 'lives_of_others.srt'

# I've lost my umlauts. 
f=codecs.open(infile, 'r', 'ISO-8859-1')
#f=codecs.open(infile, 'r', 'windows-1252')
        
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


words = {}

st = f.readlines()
for line in st:
    # is this a text line?

    line = clean_line(line)
    if len(line) > 0:
        add_words(line, words) 
        #print ":",line, ":"


words_sorted = sorted(words.iteritems(), key=operator.itemgetter(1))
import pdb
for w,c in words_sorted:
    print "%s\t%s" % (w, c)
    #if re.search('ffne', w):
        #pdb.set_trace()
    
    #outfile.write(  "%s\t%s\n" % (w,c))
    #outfile.close()



