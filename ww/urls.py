from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    # todo: next line is a placeholder
    url(r'^add_source$', views.add_source, name='add_source'),

    url(r'^list_source', views.list_source, name='list_source'),
    url(r'^show_source/(.+[^/])', views.show_source, name='show_source'),
    url(r'^show_source', views.show_source, name='show_source'),
    url(r'^show_word/(.+[^/])', views.show_word, name='show_word'),


    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', views.home),
]
