from django.template.loader import *

context = Context()

def get_prices():
    context['cheeseburger_1'] = 3.79
    context['cheeseburger_2'] = 4.79
    context['cheeseburger_3'] = 5.99
    context['cheeseburger_4'] = 7.29
    context['grilled_cheese'] = 3.49
    context['hamburger_1'] = 3.49
    context['hamburger_2'] = 4.59
    context['hamburger_3'] = 5.99
    context['hamburger_4'] = 7.29
    context['fries'] = 2.29
    context['shake'] = 4.49
    context['drink'] = 0.99
    context['animal_fries'] = 4.79
    return context
