from models import *
import stripe
import json

stripe.api_key = "sk_test_li3UZktBt8Fc3mRghlkAw1HR" #change this based on stripe account

    
def process_order(request):

    # Get the credit card details submitted by the form
    token = json_object = json.loads(request.POST['stripeToken'])
    total_amount = request.POST['total_amount']
    
    """#get the customer id from the server; might be null
    current_user = user.objects.get(account_name=request.session.get('user_name'))
    
    #stripe_id = current_user.stripe_id
    
    #email = current_user.email
    
    #if the customer does not have a credit card token
    #if stripe_id == None:
        # Create a Customer
    customer = stripe.Customer.create(
        card=token,
        description="in n out"
    )
        #stripe_id = customer.id
        #current_user.stripe_id = stripe_id
        #current_user.save()
        
    
    # Charge the Customer instead of the card
    stripe.Charge.create(
        amount=total_amount, # in cents
        currency="usd",
        customer=customer.id
    )
    
    return customer.id"""
    
    #current_user = user.objects.get(account_name=request.session.get('user_name'))
    
    #stripe_id = current_user.stripe_id
    
    #email = current_user.email
    
    #if the customer does not have a credit card token
    #if stripe_id == None:
        # Create a Customer
    try:
        customer = stripe.Customer.create(
        card=token['id'],
        description="in n out"
        )
    except stripe.CardError, e:
        # Since it's a decline, stripe.CardError will be caught
        string = ""
        body = e.json_body
        err  = body['error']

        string+= "Status is: %s<br>" % e.http_status
        string+= "Type is: %s<br>" % err['type']
        string+= "Code is: %s<br>" % err['code']
        # param is '' in this case
        string+= "Param is: %s<br>" % err['param']
        string+= "Message is: %s" % err['message']
        string+=" <br><br> "+str(token)
        return string
    #stripe_id = customer.id
    #current_user.stripe_id = stripe_id
    #current_user.save()

    # Create the charge on Stripe's servers - this will charge the user's card
    try:
      charge = stripe.Charge.create(
        amount=total_amount, # in cents
        currency="usd",
        customer=customer.id
    )
    except stripe.CardError, e:
        # The card has been declined
        return str(e)+" <br><br> "+str(token)

    return "success!"



