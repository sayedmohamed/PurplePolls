from django.conf.urls import patterns, url

from hello import views

urlpatterns = patterns('',
                       url(r'^$', views.say_hello, name='say_hello'),
                       )

