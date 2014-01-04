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
    
    current_user = user.objects.get(account_name=request.session.get('user_name'))

    #stripe_id = current_user.stripe_id
    
    #email = current_user.email
    
    #if the customer does not have a credit card token
    #if stripe_id == None:
        # Create a Customer

    # Try to create customer with the token ID
    try:
        customer = stripe.Customer.create(
        card=token['id'],
        description="in n out"
        )
    except stripe.CardError, e:
        return str(e)+" <br><br> "+str(token)

    # Create the charge on Stripe's servers - this will charge the user's card
    # (charge customer, not card)
    try:
      charge = stripe.Charge.create(
        amount=total_amount, # in cents
        currency="usd",
        customer=customer.id
    )
    except stripe.CardError, e:
        return str(e)+" <br><br> "+str(token)



    #create new order
    order_entry = orders(
                credit_card_token=token['id'], 
                user= current_user.id, # get user id from session.
                total_amount=total_amount
                )
    order_entry.save()

    # get id from order to assign to each order_part
    last_id = orders.objects.latest('id').id

    #string = ""
    for order in request.session['orders']:
        current_order_part = request.session['orders'][order]

        # Not all orders have type
        if 'type' in current_order_part: 
            type_entry = current_order_part['type']
        else:
            type_entry = ""

        order_part_entry = order_part(
                    order_id = current_order_part['id'],
                    food = current_order_part['food'],
                    price = current_order_part['price'],
                    animal_style = current_order_part['animal'],
                    food_type = type_entry,
                    desc = current_order_part['desc'],
                    order_num = last_id
                    )
        order_part_entry.save()


    """# Save orders to the database (once charge goes through)
    order_string = ""
    for thing in request.session['orders']:
        order_string+=str(request.session['orders'][thing])+" "
    return order_string"""

    return "success" # otherwise, will redirect to error page



