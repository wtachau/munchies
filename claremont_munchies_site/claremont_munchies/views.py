from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db.models import Q
#from pytz import timezone
from models import *
from stripe_payment import *
import os
import json
from prices import *
from view_helper import *
from datetime import datetime, tzinfo, timedelta
from twilio.rest import TwilioRestClient


# called from checkout. Process payment, save order, return "thanks" page if successful
def process(request):
     #user purchased the cart
    if request.method == 'POST': 
        if request.POST['delivery_location'] == 'change':
            newlocation = user.objects.get(account_name=request.session['user_name'])
            if 'register_location_dorm' in request.POST:
                newlocation.location = str(request.POST['register_location'])+" > "+str(request.POST['register_location_dorm'])
            else:
                newlocation.location = str(request.POST['register_location'])+" > "+str(request.POST['register_location_other'])
            newlocation.save()
        result = process_order(request)
        # and clear orders
        request.session['orders'] = {}
        request.session['order_total'] = 0
        if result == "success":
            return HttpResponseRedirect("thanks")
    # if something went wrong
    return HttpResponseRedirect("error")

# after checkout
def thankyou(request):
    context['order_num'] = orders.objects.latest('id').id
    return render_to_response('thankyou.html', context, RequestContext(request))

# if anything goes wrong
def error(request):
    return render_to_response('500.html', context, RequestContext(request))

# logs user out, send to landing page
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
  
# Send user to order page, also handle all additions to session order storage          
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

# grab orders and send to checkout page
def checkout(request):

    #redirect to landing page if they are not logged in
    if not is_logged_in(request):
        return send_to_landing_page(request)    
    
    if 'order_total' in request.session:
        total = request.session.get('order_total')
        context['order_total_stripe'] = total*100
        context['order_total'] = "%0.2f" % total
        context['tip_suggestion'] = "20% = $"+str("%.02f"% (float(total)/5))
        context['orders'] = request.session['orders'] # give the page all session orders 
        context['location'] = user.objects.filter(account_name=request.session['user_name']).values('location')[0]['location'] # look up from database
           
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
            context['username'] = request.POST['register_name']
            context['password'] = request.POST['register_password']    
            context['password_2'] = request.POST['register_password_2'] 
            context['fname'] = request.POST['register_fname']
            context['lname'] = request.POST['register_lname']
            context['phone_num'] = request.POST['register_phone']
            if 'register_location_dorm' in request.POST:
                context['address'] = str(request.POST['register_location'])+" > "+str(request.POST['register_location_dorm'])
            else:
                context['address'] = str(request.POST['register_location'])+" > "+str(request.POST['register_location_other'])
        
            #check the registration against the database
            valid_registration = enter_user(request,context)  

            #user commits a valid registration
            if valid_registration == 0:
                request.session['orders'] = {}
                request.session['order_total'] = 0
                return HttpResponseRedirect("/order")
            #user already exists
            elif valid_registration == 1:
                warning['warning'] = '*That User Already Exists'
                return render_to_response('landing_page.html', warning, RequestContext(request))
            #passwords do not match
            elif valid_registration == 2:
                warning['warning'] = '*The Passwords Do Not Match'
                return render_to_response('landing_page.html', warning, RequestContext(request))  
            #account name contains a space
            elif valid_registration == 3:
                warning['warning'] = '*Account Names Must Not Contain Spaces'
                return render_to_response('landing_page.html', warning, RequestContext(request))            
            #password contains a space
            elif valid_registration == 4:
                warning['warning'] = '*Passwords Must Not Contain Spaces'
                return render_to_response('landing_page.html', warning, RequestContext(request))              
        
        
        #check that the post request was for login
        if 'login_name' in request.POST:
            #gather post values
            context['username'] = request.POST['login_name']
            context['password'] = request.POST['login_password']            
            
            #login the user
            if check_login(request, context):
                request.session['orders'] = {}
                request.session['order_total'] = 0
                return HttpResponseRedirect("/order")
            else:
                warning['warning'] = '*Invalid Email or Password'
                return render_to_response('landing_page.html', warning, RequestContext(request))        
        
    #the method was not a post so load the regular page
    warning['warning'] = ''
    return render_to_response('landing_page.html', RequestContext(request))

# for the drivers - check status of orders
def drivers(request):
    # PST class to make times correct
    class PST(tzinfo):
            def utcoffset(self, dt): 
                return timedelta(hours=-8)
            def dst(self, dt):
                # DST starts last Sunday in March
                d = datetime(dt.year, 4, 1)   # ends last Sunday in October
                self.dston = d - timedelta(days=d.weekday() + 1)
                d = datetime(dt.year, 11, 1)
                self.dstoff = d - timedelta(days=d.weekday() + 1)
                if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
                    return timedelta(hours=9)
                else:
                    return timedelta(hours=-8)

    # First get all orders from today
    today = datetime.today().date()
    todays_orders = orders.objects.filter(Q(date__day=today.day) | Q(date__day=(today.day-1)),
                                        date__year = today.year,
                                        date__month=today.month, 
                                        )
    orders_list = []
    for index, cur_order in enumerate(todays_orders):
        this_order = {}
        this_order['deets'] = cur_order

        
        this_order['time'] = cur_order.date.astimezone(PST()).strftime('%b %d @ %I:%M %p')

        # add its parts
        order_parts = order_part.objects.filter(order_num=cur_order.id)
        this_order['parts'] = order_parts

        # get who ordered it
        orderer = user.objects.get(id=cur_order.user)
        this_order['name'] = str(orderer.first_name)+" "+str(orderer.last_name)
        this_order['number'] = "(%s%s%s) %s%s%s-%s%s%s%s" % tuple(orderer.phone_num)

        # add this to orders
        orders_list.append(this_order)

    # sort by id num
    context['list_orders'] = sorted(orders_list, key=lambda order: order['deets'].id)
    return render_to_response('drivers.html', context, RequestContext(request))

# When drivers update status of orders
def update_orders(request):

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACc287ec5d974fe942268f46b97d4c40cf"
    auth_token  = "d1c4702f9dd2dfa7071ec729fb8bd78b"
    client = TwilioRestClient(account_sid, auth_token)
    our_number = "+12137853417"

    for post in request.POST:
        if "order_num_" in post:

            cur_order = orders.objects.get(id=post.split("order_num_")[1])
            cur_user = user.objects.get(id=cur_order.user)
            db_status = cur_order.status
            post_status = request.POST[post]
            order_num = post.split("order_num_")[1]
            to_number = cur_user.phone_num

            # by default, set new status to be what was in db
            new_status = db_status

            if post_status == "order_assigned":
                # if the status in db is 'placed'
                if db_status == "order_placed" :
                    body = "Hi %s! The driver has left to pick up your order from Claremont Munchies." % cur_user.first_name
                    message = client.messages.create(body=body,
                        to="+1"+str(to_number),
                        from_=our_number)
                    # and set new status to be what was posted
                    new_status = post_status

            if post_status == "order_incar":
                # if status in db is 'assigned'
                if db_status == "order_assigned":
                    body = "Hi %s! Your order from Claremont Munchies is on its way back from In-N-Out." % cur_user.first_name
                    message = client.messages.create(body=body,
                        to="+1"+str(to_number),
                        from_=our_number)
                    # and set new status to be what was posted
                    new_status = post_status

            if post_status == "order_delivered":
                # whenever post is to delivered, save it
                new_status = post_status

            cur_order.status = new_status
            cur_order.save()

    return HttpResponseRedirect("drivers")

def terms(request):
    return render_to_response('terms.html', context, RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html', context, RequestContext(request))

def aboutus(request):
    return render_to_response('aboutus.html', context, RequestContext(request))
