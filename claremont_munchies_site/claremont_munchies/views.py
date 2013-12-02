from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
from stripe_payment import *
import os
import json
from prices import *
from view_helper import *


def logout(request):
    request.session['logged_in'] = False
    request.session['user_name'] = ''
    return HttpResponseRedirect("/")

def updateTotal(request):
    if 'orders' in request.session:
        if 'order_total' in request.session:
            request.session['order_total'] = 0
            for k,v in request.session['orders'].iteritems():
                request.session['order_total'] += v.get('price')
        else:
            request.session['order_total'] = 0
            
def order_form(request):


    #redirect to landing page if they are not logged in
    if not is_logged_in(request):
        return send_to_landing_page(request)    

    context = get_prices()
    if 'orders' in request.session and 'order_total' in request.session:
        context['orders'] = request.session['orders'] # give the page all session orders
        context['subtotal'] = "$"+str(request.session['order_total'])
    
    if request.method == 'POST':
        
        data = request.POST.dict() # grab queryDict object, put into dict
        
        # if we were told to delete an item, delete it from session
        if 'delete' in data:
            delete_object = data['delete']
            if delete_object in request.session['orders']:
                del request.session['orders'][delete_object]
                
            updateTotal(request)
            return HttpResponse();
        # otherwise, we're creating a new item. Add it to the session dictionary
        else:
            json_object = json.loads(data['object']) # grab the object (leave behind csrf token)
        
            # initialize request session if it's not there already
            if 'orders' not in request.session:
                request.session['orders'] = {}
            if 'order_total' not in request.session:
                request.session['order_total'] = 0
                    
            index = json_object['id']
            
            #request.session['orders'] = {} #ONLY TO FLUSH SESSION ORDERS
            request.session['orders'][index] = json_object
            
            updateTotal(request)
            return HttpResponse();
            #return HttpResponse("<html>"+str(request.session['orders'])+"      "+str(index)+" "+ str(request.session.items())+ "</html>")
    
    return render_to_response('order_form.html', context, RequestContext(request))

def checkout(request):
    
    #redirect to landing page if they are not logged in
    if not is_logged_in(request):
        return send_to_landing_page(request)    
    
    total = request.session.get('order_total')
    context['order_total'] = total*100
    context['order_total_desc'] = '$'+str(total)
    
    #user purchased the cart
    if request.method == 'POST':
        if 'stripeToken' in request.POST:      
            token = process_order(request, context['order_total'])
            return HttpResponse(token)
        
    #user came from our order form
    if 'orders' in request.session:
        context['orders'] = request.session['orders'] # give the page all session orders    
    return render_to_response('checkout.html', context, RequestContext(request))
    
#checks the integrity of login/register credentials
def landing_page(request):
    
    #redirect the user to the order page if they are logged in
    if is_logged_in(request):
        return send_to_order(request)
    
    if request.method == 'POST':
        
        #check that the post request was for registration
        if 'register_name' in request.POST:
            #gather post values
            context['name'] = request.POST['register_name']
            context['password'] = request.POST['register_password']    
            context['password_2'] = request.POST['register_password_2'] 
        
            #check the registration against the database
            valid_registration = enter_user(request,context)  

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
            #account name contains a space
            elif valid_registration == 3:
                warning['warning'] = 'Account Names Must Not Contain Spaces'
                return render_to_response('landing_page.html', warning, RequestContext(request))            
            #password contains a space
            elif valid_registration == 4:
                warning['warning'] = 'Passwords Must Not Contain Spaces'
                return render_to_response('landing_page.html', warning, RequestContext(request))              
        
        
        #check that the post request was for login
        if 'login_name' in request.POST:
            #gather post values
            context['name'] = request.POST['login_name']
            context['password'] = request.POST['login_password']            
            
            #login the user
            if check_login(request, context):
                return send_to_order(request)
            else:
                warning['warning'] = 'Invalid Email or Password'
                return render_to_response('landing_page.html', warning, RequestContext(request))        
        
    #the method was not a post so load the regular page
    warning['warning'] = ''
    return render_to_response('landing_page.html', RequestContext(request))



