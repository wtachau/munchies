from django.conf.urls import patterns, include, url
from claremont_munchies.views import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', landing_page),
    url(r'^order$', order_form),
    url(r'^login$', login),
    url(r'^register$', register),
    # url(r'^$', 'claremont_munchies_site.views.home', name='home'),
    # url(r'^claremont_munchies_site/', include('claremont_munchies_site.foo.urls')),
      
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
