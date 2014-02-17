from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ntsstock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',include('stockmanage.urls',namespace='stockmanage')),
    url(r'^stockmanage/',include('stockmanage.urls',namespace='stockmanage')),
    url(r'^admin/', include(admin.site.urls)),
)
