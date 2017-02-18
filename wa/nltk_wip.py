##### -*- coding: utf-8 -*-

import pdb

import sys
import nltk

from nltk.corpus import brown
from nltk import sent_tokenize, word_tokenize, pos_tag



f = open('besser_gehts_nicht.txt')
f = open('lives_short.txt')
#python 3 syntax f = open('besser_gehts_nicht.txt', encoding='utf-8')

raw = f.read()
print raw

from pattern.de import gender, MALE, FEMALE, NEUTRAL
from pattern.de import article, DEFINITE, FEMALE, OBJECT
print gender('Katze')
print article('Katze', DEFINITE, gender=FEMALE, role=OBJECT)

from pattern.de import conjugate
from pattern.de import INFINITIVE, PRESENT, SG, SUBJUNCTIVE
print conjugate('sehe', INFINITIVE)
print conjugate('sehen', PRESENT, 1, SG, mood=SUBJUNCTIVE) 

from pattern.de import parse,parsetree, split

"""
import pattern.de
pattern.de.verbs - 1962 verbs. 
pattern.de.tenses 
pattern.de.tenses('erblicken')
pattern.de.conjugate.__doc__


"""


"""
lst=parse(raw)
(Pdb) split(lst)[0]
Sentence('Stehen/VB/B-VP/O bleiben/VB/I-VP/O !/./O/O')
"""
lst = parse(raw)
for sent in split(lst):
    print "sent.string: ", sent.string
   
pdb.set_trace()



sys.exit(2)
s = parsetree(raw)
print "sentences now"
for sentence in s:
    print "sentence: ", sentence
    
    for chunk in sentence.chunks:
        print  "sentence: ", " ".join([w.string for w in chunk.words])
        #print "\tchunk type: ", chunk.type, [(w.string, w.type) for w in chunk.words]
        pdb.set_trace() 

    #print sentence 

pdb.set_trace()

#print("file has ", len(word_tokenize(raw)), "words.")
#print word_tokenize(raw)

lst1 = nltk.Text('besser_gehts_nicht.txt')
lst = nltk.Text(raw)
print lst.concordance('s')
print "length:", len(lst)
print "besser: ", lst.concordance('besser')
print "gehts: ", lst.concordance('gehts')
pdb.set_trace()
lst.concordance()


#wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]

#print wordlist
pdb.set_trace()
sys.exit(2)



f=open("besser_gehts_nicht.txt", "r")
text = " ".join(f.readlines())
#tokens = word_tokenize(text)
#sents = sent_tokenize(text)


print text
print tokens
#print sents
pdb.set_trace()


sys.exit(2)
lst1 = brown.tagged_words()
#lst1 = brown.tagged_words()[0:100]
print len(lst1)
#1161192
lst2=set(lst1)
print len(lst2)
#56057

pos = {}
for w in lst2:
    print "w:",w
    print "\tw[1]:",w[1]
    try:
        if w[1] in pos:
            pos[w[1]] +=1
        else:
            pos[w[1]] =1
    except:
        print "fail"
        pdb.set_trace()

print "pos", pos
cnt = 1
for p in pos.keys():
    print "%i: %s = %i" % (cnt,p, pos[p])
    cnt+=1
#lst = [f[1] for f in brown.tagged_words()]
