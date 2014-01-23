from django.template.loader import *

context = Context()

def get_prices():
    context['cheeseburger_1'] = 5.49
    context['cheeseburger_2'] = 6.79
    context['cheeseburger_3'] = 7.99
    context['cheeseburger_4'] = 8.99
    context['grilled_cheese'] = 4.99
    context['hamburger_1'] = 4.99
    context['hamburger_2'] = 6.29
    context['hamburger_3'] = 7.49
    context['hamburger_4'] = 8.49
    context['fries'] = 2.49
    context['shake'] = 4.99
    context['drink'] = 0.99
    context['animal_fries'] = 4.99
    return context
