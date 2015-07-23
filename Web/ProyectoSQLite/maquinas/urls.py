from django.conf.urls import include, url
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from maquinas.views import bigform
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	#url(r'^(?P<salon_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<salon_id>[0-9]+)/(?P<pc_id>[0-9]+)/$', views.lecturas, name='lecturas'),
	#url(r'^(?P<salon_id>[0-9]+)/agregarpc/$', views.agregarpc, name='agregarpc'),
	#url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^$', auth_views.login, {'template_name': 'maquinas/index.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/maquinas/'}, name='logout'),
	url(r'^bigform/$', bigform, name='bigform'),
	url(r'^/$', views.index, name='index'),
	url(r'^(?P<pk>[a-z0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^(?P<pc_id>[a-z0-9]+)/results/$', views.results, name='results'),
	#url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
]