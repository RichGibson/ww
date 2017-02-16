#### -*- coding: utf-8 -*
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#from django.shortcuts import render_to_response
from django.db.models import Count
from django.db.models import F
#from django.db.models import get_app, get_models
from django.apps import apps

from ww.models import Word, Source, SourceType, WordSource
import sys

# todo what does :ps do

def home(request):
    return render(request, 'ww/home.html', {})

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
    lst = WordSource.objects.filter(source=source)
    # select ww_word.word, count(*) as cnt from ww_word, ww_wordsource where ww_word.id=ww.wordsource.word_id and ww_wordsource.source_id=10 group by word order by cnt desc;
    source=slst[0].name
    title = "Show ", source
    return render(request, 'ww/show_source.html', {"title":title, "lst":lst, "source":source})

def add_source(request):
    title = "Add Source"
    lst = []
    return render(request, 'ww/add_source.html', {"title":title, "lst":lst})

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
