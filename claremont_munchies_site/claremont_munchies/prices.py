from django.template.loader import *

context = Context()

def get_prices():
    # burgers
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

    #mexican
    context['burrito_carne'] = 6.49
    context['burrito_beans'] = 4.99
    context['burrito_beef'] = 5.99
    context['burrito_chicken'] = 5.99
    context['taco_beef'] = 3.29
    context['taco_chicken'] = 3.29
    context['taco_carne'] = 3.79
    context['taco_tacquitos'] = 4.99
    context['quesadilla_cheese'] = 4.99
    context['quesadilla_chicken'] = 6.29
    context['quesadilla_beef'] = 6.29
    return context
