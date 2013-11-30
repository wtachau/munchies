from models import *
import stripe

stripe.api_key = "sk_test_lOyq2bIOtEfGJR6yoEsJjA3h"


def process_order(request):
    
    if 'stripeToken' not in request.POST:
        return ''
    
    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']
    
    #get the customer id from the server; might be null
    current_user = user.objects.get(account_name=request.session.get('user_name'))
    
    #stripe_id = current_user.stripe_id
    
    #email = current_user.email
    
    #if the customer does not have a credit card token
    #if stripe_id == None:
        # Create a Customer
    customer = stripe.Customer.create(
        card=token,
        description="bitchass"
    )
        #stripe_id = customer.id
        #current_user.stripe_id = stripe_id
        #current_user.save()
        
    
    # Charge the Customer instead of the card
    stripe.Charge.create(
        amount=20000, # in cents
        currency="usd",
        customer=customer.id
    )
    
    return customer.id



