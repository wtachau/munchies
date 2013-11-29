from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
#our login file to verify credentials
from login import *
from register import *

#initialize the same context item for all pages
context = Context()
warning = Context()

def hello(request):
    return HttpResponse("<h1>Hello Page</h1>Hello world")

def order_form(request):
    t = get_template('order_form.html')
    html = t.render(Context())
    return HttpResponse(html)

def landing_page(request):
    if request.method == 'POST':
        
        #check if the user is trying to register
        context['name'] = request.POST['register_name']
        context['password'] = request.POST['register_password']    
        context['password_2'] = request.POST['register_password_2'] 
        
        if len(context['name']) > 0:
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
        
        #check if the user is trying to login
        context['name'] = request.POST['login_name']
        context['password'] = request.POST['login_password']
        
        if len(context['name']) > 0:
            is_logged_in = check_login(context)
            if is_logged_in:
                return HttpResponseRedirect("/order")
            else:
                warning['warning'] = 'Invalid Email or Password'
                return render_to_response('landing_page.html', warning, RequestContext(request))        
        
    #the method was not a post so load the regular page
    warning['warning'] = ''
    return render_to_response('landing_page.html', RequestContext(request))
