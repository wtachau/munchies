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

def hello(request):
    return HttpResponse("<h1>Hello Page</h1>Hello world")

def order_form(request):
    t = get_template('order_form.html')
    html = t.render(Context())
    return HttpResponse(html)

def landing_page(request):
     
    return render_to_response('landing_page.html', RequestContext(request))

#register a new user; if data already exists, send them back to index with message
def register(request):
    
    context['name'] = request.POST['register_name']
    context['password'] = request.POST['register_password']    
    context['password_2'] = request.POST['register_password_2'] 
    
    valid_registration = enter_user(context)
    
    if valid_registration == 0:
        return HttpResponseRedirect("/order")
    elif valid_registration == 1:    
        return HttpResponse('<html><p>That user already exists!</p></html>')
    elif valid_registration == 2:
        return HttpResponse('<html><p>Your passwords do not match!</p></html>')
    

#grab the contents of the login box and verify that they are in the database
def login(request):
    
    context['name'] = request.POST['login_name']
    context['password'] = request.POST['login_password']
    
    #check if the given credentials are in our database
    is_logged_in = check_login(context)

    if is_logged_in:
        return HttpResponseRedirect("/order")
    
    else:    
        return HttpResponse('<html><p>You are not a registered user!</p></html>')
