from django.db import models
from models import *

#function is passed login credentials to be checked with the database
def check_login(l_c):
    validate = user.objects.filter(name=l_c['name'], password=l_c['password']).count()
    if validate > 0:
        return True
    else:
        return False