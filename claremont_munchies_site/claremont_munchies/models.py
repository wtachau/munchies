from django.db import models
# Create your models here

class user(models.Model):
    account_name = models.CharField(max_length=60)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    location = models.CharField(max_length=255, null=True)
    claremont_id_number = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=255)
    stripe_id = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class order_part(models.Model):
    order_id = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    price = models.IntegerField(max_length=3)
    animal_style = models.CharField(max_length=11)
    food_type = models.CharField(max_length=255)
    desc = models.CharField(max_length=500)
    order_num = models.IntegerField()
    
class orders(models.Model):
    credit_card_token = models.CharField(max_length=255)
    user = models.CharField(max_length=11)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    total_amount = models.IntegerField()

class deals(models.Model):
    deal_type = models.CharField(max_length=11)
    deal_value = models.IntegerField()

class dealInstances(models.Model):
    user_id = models.IntegerField()
    deal_id = models.IntegerField()

    
    