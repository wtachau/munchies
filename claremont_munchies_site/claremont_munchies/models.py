from django.db import models
# Create your models here.


class user(models.Model):
    account_name = models.CharField(max_length=60)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    location = models.CharField(max_length=255, null=True)
    claremont_id_number = models.CharField(max_length=20, null=True)
    credit_card_token = models.CharField(null=True, max_length=255)
    
    
    
    