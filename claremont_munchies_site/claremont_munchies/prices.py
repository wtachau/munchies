from django.template.loader import *

context = Context()

def get_prices():
    context['cheeseburger_1'] = 3.99
    context['cheeseburger_2'] = 5.29
    context['cheeseburger_3'] = 6.49
    context['cheeseburger_4'] = 7.99
    context['grilled_cheese'] = 3.49
    context['hamburger_1'] = 3.49
    context['hamburger_2'] = 4.89
    context['hamburger_3'] = 6.49
    context['hamburger_4'] = 7.49
    context['fries'] = 2.39
    context['shake'] = 4.49
    context['drink'] = 0.99
    context['animal_fries'] = 4.99
    return context
