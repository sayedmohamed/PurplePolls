from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.index_new, name='index_new'),
    url(r'^(?P<pk>\d+)/$', views.poll_detail, name='poll_detail'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='poll_detail_vote'),
)

