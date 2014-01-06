from django.template.loader import *

context = Context()

def get_prices():
    context['cheeseburger_1'] = 5
    context['cheeseburger_2'] = 6
    context['cheeseburger_3'] = 7.5
    context['cheeseburger_4'] = 8.5
    context['hamburger_1'] = 5
    context['hamburger_2'] = 6
    context['hamburger_3'] = 7.5
    context['hamburger_4'] = 8.5
    context['fries'] = 3
    context['shake'] = 5
    context['drink'] = 1
    context['animal'] = 2.5
    return context
