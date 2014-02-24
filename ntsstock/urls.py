from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'stockmanage.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',include('stockmanage.urls',namespace='stockmanage')),
    url(r'^stockmanage/',include('stockmanage.urls',namespace='stockmanage')),
    url(r'^admin/', include(admin.site.urls)),
)
