from django.conf.urls import patterns, include, url
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^polls/', include('polls.urls', namespace='polls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^hello/', include('hello.urls')),
                       )

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)