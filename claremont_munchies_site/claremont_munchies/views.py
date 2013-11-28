from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import *

import datetime


def hello(request):
    return HttpResponse("<h1>Hello Page</h1>Hello world")

def order_form(request):
    t = get_template('order_form.html')
    html = t.render(Context())
    return HttpResponse(html) 