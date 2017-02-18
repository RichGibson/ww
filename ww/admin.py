
from django.contrib import admin
from django.urls import reverse
#import django.forms 
from django.forms import ModelForm

from .models import Word, Source, SourceType, WordSource, Sentence, WordSentence

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Word._meta.get_fields()] )
    pass

@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Word._meta.get_fields()] )
    pass

@admin.register(WordSentence)
class WordSentenceAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Word._meta.get_fields()] )
    pass

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    #list_display = ( [f.name for f in Source._meta.get_fields()] )
    pass

@admin.register(SourceType)
class SourceTypeAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in SourceType._meta.get_fields()] )
    pass

@admin.register(WordSource)
class WordSourceTypeAdmin(admin.ModelAdmin):
    #list_display = (source, word, cnt )
    list_display = ( [f.name for f in WordSource._meta.get_fields()] )
    pass
