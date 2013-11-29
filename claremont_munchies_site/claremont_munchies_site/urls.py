from django.conf.urls import patterns, include, url
from claremont_munchies.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url('', '')
    # url(r'^$', 'claremont_munchies_site.views.home', name='home'),
    # url(r'^claremont_munchies_site/', include('claremont_munchies_site.foo.urls')),
      #url(r'^$', order_form),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
