from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *

context = Context()
warning = Context()

"""These are helper functions for our views.py file"""

#helper functions
def is_logged_in(request):
    request.session.get('logged_in')


def ask_to_login(request):
    warning['warning'] = 'You Must Login'
    return render_to_response('landing_page.html', context, RequestContext(request))

def send_to_order(request):
    return HttpResponseRedirect("/order")



#function is passed login credentials to be checked with the database

def enter_user(request,login_credentials):
    
    #value to be entered into db; other fields null
    entry = user(account_name=login_credentials['name'].lower(), password=login_credentials['password'])
    
    #check if user is already in db
    validate = user.objects.filter(account_name=login_credentials['name']).count()
    
    #user is already in the database
    if validate > 0:
        return 1
    #the passwords do not match
    elif login_credentials['password'] != login_credentials['password_2']:
        return 2
    #if account name has a space
    elif ' ' in login_credentials['name']:
        return 3
    #password has a space
    elif ' ' in login_credentials['password']:
        return 4    
    #save the entry into the database
    else:
        request.session['logged_in'] = True
        entry.save()
        return 0
    

#function is passed login credentials to be checked with the database
def check_login(request, l_c):
    validate = user.objects.filter(account_name=l_c['name'].lower(), password=l_c['password']).count()
    if validate > 0:
        request.session['logged_in'] = True
        return True
    else:
        return False