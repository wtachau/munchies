from django.db import models
# Create your models here.


class user(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    #the card identification number
    card = models.IntegerField(null=True)
    password = models.CharField(max_length=60)

    
class credit_card(models.Model):
    card_number = models.IntegerField()
    exp_date_month = models.IntegerField()
    exp_date_year = models.IntegerField()
    csv = models.IntegerField()
    #billing address identification number
    billing_address = models.IntegerField()

class billing_address(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.IntegerField()
    street_address = models.CharField(max_length=255)
    
    
    