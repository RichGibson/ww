
from django.contrib import admin
from django.urls import reverse
#import django.forms 
from django.forms import ModelForm

from .models import Word, Source, SourceType, WordSource

@admin.register(Word)
class PropertyAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Property._meta.get_fields()] )
    pass

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Contact._meta.get_fields()] )
    pass

@admin.register(SourceType)
class SourceAdmin(admin.ModelAdmin):
    #list_display = ( [f.name for f in Contact._meta.get_fields()] )
    pass

@admin.register(WordSource)
class WordSourceTypeAdmin(admin.ModelAdmin):
    #list_display = ( )
    pass
