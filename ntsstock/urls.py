from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
   #url(r'^account/logout/'),
    url(r'^$', 'stockmanage.views.index', name='index')
    ,url(r'^accounts/login.+','django.contrib.auth.views.login',{'template_name':'stockmanage/login.html'},)   
    ,url(r'^accounts/logout.+','django.contrib.auth.views.logout',{'template_name':'stockmanage/login.html'}, )
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',include('stockmanage.urls',namespace='stockmanage')),
    ,url(r'^stockmanage/',include('stockmanage.urls',namespace='stockmanage'))
    ,url(r'^admin/', include(admin.site.urls))
)
