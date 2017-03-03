import pdb
import re
from nltk.corpus import inaugural 
import nltk

lst=inaugural.fileids()
print lst
lst2 = [ (l.split('-')[0], re.sub('\.txt','', l.split('-')[1])) for l in lst]
print lst2
raw = open('gesicht.txt').read().decode('utf-8')
print raw

thes = open('openthesaurus.txt').read().decode('utf-8')
pdb.set_trace()
