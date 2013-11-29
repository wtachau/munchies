from django.db import models
from models import *

#function is passed login credentials to be checked with the database
def enter_user(l_c):
    entry = user(name=l_c['name'], location='', card=0, password=l_c['password'])
    validate = user.objects.filter(name=l_c['name'], password=l_c['password']).count()
    if validate > 0:
        return 1
    
    elif l_c['password'] != l_c['password_2']:
        return 2
    
    else:
        entry.save()
        return 0