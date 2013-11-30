from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
import os
#our login file to verify credentials
from login import *
from register import *
from prices import *
#url encoding issues
import json

#initialize the same context item for all pages
context = Context()
warning = Context()

def hello(request):
    return HttpResponse("<h1>Hello Page</h1>Hello world")

def order_form(request):
    context = get_prices()
    context['css_root'] = os.getcwd()+'/templates'
    return render_to_response('order_form.html', context, RequestContext(request))

def checkout(request):
    if request.method == 'POST':
        #context['raw_data'] = request.get_raw_post_data
        #q = QueryDict(request.POST)
        #context['raw_data'] = request
        
        querydict_data = request.POST
        json_data = querydict_data['json_string']
        context['raw_data'] = json.loads(json_data)
        
        #urllib.unquote(request.body).decode('utf8') 
        
        #for key in request.POST:
        #    context['raw_data'] = context['raw_data'] + "---" + key
        return render_to_response('checkout.html', context, RequestContext(request))
    else:
        return render_to_response('checkout.html', context)


#checks the integrity of login/register credentials
def landing_page(request):
    if request.method == 'POST':
        
        #check that the post request was for registration
        if 'register_name' in request.POST:
            #gather post values
            context['name'] = request.POST['register_name']
            context['password'] = request.POST['register_password']    
            context['password_2'] = request.POST['register_password_2'] 
        
        
            #check the registration against the database
            valid_registration = enter_user(context)  
            #user commits a valid registration
            if valid_registration == 0:
                return HttpResponseRedirect("/order")
            #user already exists
            elif valid_registration == 1:
                warning['warning'] = 'That User Already Exists'
                return render_to_response('landing_page.html', warning, RequestContext(request))
            #passwords do not match
            elif valid_registration == 2:
                warning['warning'] = 'The Passwords Do Not Match'
                return render_to_response('landing_page.html', warning, RequestContext(request))        
        
        
        
        #check that the post request was for login
        if 'login_name' in request.POST:
            #gather post values
            context['name'] = request.POST['login_name']
            context['password'] = request.POST['login_password']            
            is_logged_in = check_login(context)
            if is_logged_in:
                return HttpResponseRedirect("/order")
            else:
                warning['warning'] = 'Invalid Email or Password'
                return render_to_response('landing_page.html', warning, RequestContext(request))        
        
    #the method was not a post so load the regular page
    warning['warning'] = ''
    return render_to_response('landing_page.html', RequestContext(request))
