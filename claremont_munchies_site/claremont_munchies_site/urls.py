from django.conf.urls import patterns, include, url
from claremont_munchies.views import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', landing_page),
    url(r'^order$', order_form),
    url(r'checkout$', checkout),
    url(r'^logout$', logout),
    url(r'^thanks$', thankyou),
    url(r'^process$', process),
    url(r'^error$', error),
    url(r'^drivers', drivers),
    url(r'^update_orders', update_orders),
    url(r'^privacy', privacy),
    url(r'^terms', terms),
    url(r'^aboutus', aboutus),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.STATIC_URL+'images/favicon.ico'}),
    # url(r'^$', 'claremont_munchies_site.views.home', name='home'),
    # url(r'^claremont_munchies_site/', include('claremont_munchies_site.foo.urls')),
      
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)