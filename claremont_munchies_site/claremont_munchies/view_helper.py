from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from models import *

context = Context()
warning = Context()

"""These are helper functions for our views.py file"""


#helper functions
def is_logged_in(request):
    return request.session.get('logged_in') and ('user_name' in request.session)

def send_to_order(request):
    return HttpResponseRedirect("/order")

def send_to_landing_page(request):
    return HttpResponseRedirect('/')

#function is passed login credentials to be checked with the database
def enter_user(request, login_credentials):
    
    #value to be entered into db; other fields null
    entry = user(account_name=login_credentials['username'].lower(), 
        password=login_credentials['password'], #use make_password for encryption
        first_name=login_credentials['fname'],
        last_name=login_credentials['lname'],
        location=login_credentials['address'],
        phone_num=login_credentials['phone_num']
        )
    
    #check if user is already in db
    validate = user.objects.filter(account_name=login_credentials['username']).count()
    
    
    #user is already in the database
    if validate > 0:
        return 1
    #the passwords do not match
    elif login_credentials['password'] != login_credentials['password_2']:
        return 2
    #if account name has a space
    elif ' ' in login_credentials['username']:
        return 3
    #password has a space
    elif ' ' in login_credentials['password']:
        return 4    
    #save the entry into the database
    else:
        request.session['logged_in'] = True
        request.session['user_name'] = login_credentials['username']
        entry.save()
        return 0
    

#function is passed login credentials to be checked with the database
def check_login(request, login_credentials):
    validate = user.objects.filter(account_name=login_credentials['username'].lower(), 
                                   password=login_credentials['password']).count()
    if validate > 0:
        request.session['logged_in'] = True
        request.session['user_name'] = login_credentials['username']
        return True
    else:
        return False