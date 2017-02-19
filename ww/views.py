#### -*- coding: utf-8 -*
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#from django.shortcuts import render_to_response
from django.db.models import Count
from django.db.models import F
#from django.db.models import get_app, get_models
from django.apps import apps
from django.forms import ModelForm

from django.http import HttpResponseRedirect

import enchant
d=enchant.Dict('de_DE')

from ww.models import Word, Source, SourceType, WordSource
from ww.models import Sentence, WordSentence, UserWord

import sys
import re

# todo what does :ps do

class AddSourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_type', 'fulltext', 'notes')


def home(request):
    lst = WordSource.objects.all().order_by('-cnt')[0:25]
    return render(request, 'ww/home.html', {'lst':lst})

def about(request):
    lst = WordSource.objects.all().order_by('-cnt')[0:25]
    return render(request, 'ww/about.html', {'lst':lst})

def list_source(request, source=None):
    """ list of sources """
    title = "List Source(s)"
    lst = []
    lst = Source.objects.all()
    return render(request, 'ww/list_source.html', {"title":title, "lst":lst})

def show_source(request, source=None):
    """ Detail on one source and its' words """
    lst = []
    slst = Source.objects.filter(id = source)
    if source:
        lst = WordSource.objects.filter(source=source)
    else:
        lst = WordSource.objects.all()
        #lst = Word.objects.all()

    # select ww_word.word, count(*) as cnt from ww_word, ww_wordsource where ww_word.id=ww.wordsource.word_id and ww_wordsource.source_id=10 group by word order by cnt desc;
    if source:
        source=slst[0]
    else:
        source = "All Words"
    title = "Show ", source
    return render(request, 'ww/show_source.html', {"title":title, "lst":lst, "source":source})


def clean_line(line):

    #if re.search('[a..zA..Z]', line):
    #    line = line
    #else:
    #    line = ''

    line=re.sub(':','',line)
    line=re.sub('\.','',line)
    line=re.sub('"','',line)
    line=re.sub("!",' ',line)
    line=re.sub("'",'',line)
    line=re.sub('\(',' ',line)
    line=re.sub('\)',' ',line)
    line=re.sub(',',' ',line)
    line=re.sub('\?',' ',line)
    line=re.sub('-',' ',line)
    line=re.sub('”',' ',line)
    line=re.sub('“',' ',line)
    line=re.sub('„',' ',line)
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
    todo: This is rejecting a lot of things which it should not reject.
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

def loadWords(source):
    """
    load the words in source.fulltext 
    """
    words = {}
    # throwback 'line' from file import version
    line = source.fulltext
    line = clean_line(line)
    line = line.encode('utf-8')
    for word in line.split():
        if not isWord(word):
            continue
        if word in words:
            words[word] +=1
        else:
            words[word]=1
    for word in words.keys():
        w=Word.objects.filter(word=word)
        if len(w)>0:
            w=w[0]
        else:
            w=Word()
        w.word = word
        w.save()
        ws = WordSource()
        ws.source=source
        ws.word = w
        ws.cnt = words[word]
        ws.save()
        

    

def add_source(request):
    title = "Add Source"
    lst = []
    if request.method == "POST":
        form  = AddSourceForm(request.POST)
        if form.is_valid():
            source = form.save()
            loadWords(source)
            title = "You added a source...yay for you!"
            return HttpResponseRedirect('show_source/%i' % source.id, {"title":title,  "lst":lst})
    else:
        form  = AddSourceForm()

    return render(request, 'ww/add_source.html', {"title":title, "form":form, "lst":lst})

def show_word(request, word=None):
    """ Detail on one word """
    word_lst = []
    src_lst = []
    prefix_search = ''
    suffix_search = ''
    mid_search = ''
    if request.method == "POST":
        #if POST.post
        # prefix_search, mid_search, suffix_search
        prefix_search = request.POST.get('prefix_search', '')
        suffix_search = request.POST.get('suffix_search', '')
        mid_search = request.POST.get('mid_search', '')

        print >>sys.stderr, "len word_lst: ", len(word_lst)
        word_lst = Word.objects.filter(word__iregex=r'^%s.*%s.*%s' % (prefix_search, mid_search, suffix_search) )
        if prefix_search:
            #word_lst = word_lst.filter(word__istartswith=prefix_search)
            print >>sys.stderr, "prefix len word_lst: ", len(word_lst)

        if suffix_search:
            #word_lst = word_lst.filter(word__iendswith=suffix_search)

            #word_lst = word_lst.filter(word__iregex=r'^%s.*%s.*%s' % (prefix_search, mid_search, suffix_search) )
            print >>sys.stderr, "suffix len word_lst: ", len(word_lst)

        if mid_search:
            #word_lst = word_lst.filter(word__icontains=mid_search)
            print >>sys.stderr, "mid len word_lst: ", len(word_lst)

        print >>sys.stderr, "show word in list, prefix, suffix ", prefix_search, suffix_search
        word_str = "Words matching %s-%s-%s" % (prefix_search, mid_search, suffix_search)
    else:
        if word:
            src_lst = WordSource.objects.filter(word=word)
            word_str=src_lst[0].word
        else:
            wrd_lst = WordSource.objects.all()
            word_str=wrd_lst[0].word

    sentence_lst = []
    sentence_lst = WordSentence.objects.filter(word=word)

    # todo: maybe need a SentenceSource link
    # oh, also, I don't need to write this WordSentence type models - it is a many to many deal.
    title = "Show ", word

    if len(word_lst) > 0:
        pass
    else:
        #word = word_lst[0].word
        pass

    #word = Word.objects.filter(id=word)[0].word
    return render(request, 'ww/show_word.html', {"title":title, "src_lst":src_lst, "word_lst":word_lst,"sentence_lst":sentence_lst, "word_str":word_str, "prefix_search":prefix_search, "suffix_search":suffix_search, "mid_search":mid_search})

#@login_required
def field_search(request, model):
    """ 
    Display list of fields from a passed in model, return a form with
    all of the fields.
   
    Take the form response, do a query against model.

    Start with property_search, with hard coded fields.
    """
    title = "Field search from model <b>%s</b>" % (model)
    #my_model = apps.get_model('ts', model)

    #return render(request, 'ts/simple_list.html', {"title":title, "lst":lst, "includepage":"ts/field_count.html"})

@login_required
def field_counts(request, model=None, field_name=None):
    """ 
    Take a field name and return the results of a query of the form:
    select field, count(field) from model group by field order by field

    note: this assumes application 'ts'
    """

    if not model:
        pass
    else:
        my_model = apps.get_model('ts', model)

    # value, dcount are the returned field names
    # F is magic from django.db.models
    #lst = Property.objects.annotate(value=F(field_name)).values('value').annotate(dcount=Count(field_name)).order_by(field_name)

    lst = []
    field_lst = []
    model_lst = []
    if not model:
        # return a list of models
        title = "Select a Model to see field options"
        model_lst = apps.all_models['ts'].keys()
        print >>sys.stderr, "model lst : ", model_lst

    if model and not field_name:
        # return a list of fields
        title = "Select a field in %s for a group by count" % (model)
        field_lst = [f.name for f in my_model._meta.get_fields()]

    if model and field_name:
        title = "Field %s from model %s" % (field_name, model)
        lst = my_model.objects.annotate(value=F(field_name)).values('value').annotate(dcount=Count(field_name)).order_by(field_name)

    return render(request, 'ts/simple_list.html', {"title":title, "model":model, "field_name":field_name, "lst":lst, "field_lst":field_lst, "model_lst":model_lst, "includepage":"ts/field_count.html"})

@login_required
def properties(request, filter_name=None, filter_val=None):
    title = "Property List"
    print >>sys.stderr, "filter_name: ", filter_name
    print >>sys.stderr, "filter_val: ", filter_val
    if filter_name:
        #lst = Property.objects.filter(filter = val)
        lst=Property.objects.annotate(fld=F(filter_name)).filter(fld__iexact = filter_val)
    else:
        lst = Property.objects.all()
    return render(request, 'ts/simple_list.html', {"title":title, "model":"property", "lst":lst, "includepage":"ts/property_list.html"})

def contacts(request):
    title = "Contacts List"
    lst = Contact.objects.all()
    return render(request, 'ts/simple_list.html', {"title":title, "lst":lst})

def locations(request):
    title = "Locations List"
    lst = Location.objects.all()
    return render(request, 'ts/simple_list.html', {"title":title, "lst":lst})

def organizations(request):
    title = "Organizations List"
    lst = Organzation.objects.all()
    return render(request, 'ts/simple_list.html', {"title":title, "lst":lst})
