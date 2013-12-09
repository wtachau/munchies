from django.db import models
# Create your models here.


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
    
class orders(models.Model):
    credit_card_token = models.CharField(max_length=255)
    order = models.CharField(max_length=500)
    date = models.DateField(auto_now = True, auto_now_add=True)
    total_amount = models.IntegerField()

class deals(models.Model):
    deal_type = models.CharField(max_length=11)
    deal_value = models.IntegerField()

class dealInstances(models.Model):
    user_id = models.IntegerField()
    deal_id = models.IntegerField()
    
    
    