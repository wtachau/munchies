from django.template.loader import *

context = Context()

def get_prices():
    context['cheeseburger_1'] = 11
    context['cheeseburger_2'] = 12
    context['cheeseburger_3'] = 13
    context['cheeseburger_4'] = 14
    context['hamburger_1'] = 21
    context['hamburger_2'] = 22
    context['hamburger_3'] = 23
    context['hamburger_4'] = 24
    context['fries'] = 2
    context['shake'] = 3
    context['drink_small'] = 40
    context['drink_large'] = 50
    context['animal'] = 3
    return context
