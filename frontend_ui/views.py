from django.shortcuts import render
from calculator_api.constants import CHOICES, INSTRUMENTS


def index(request):
    instruments_map = {choice[1]: INSTRUMENTS.get(choice[0])
                    for choice in CHOICES}

    return render(request, 'frontend_ui/index.html', {
        'instruments': CHOICES,
        'instruments_map': instruments_map
    })
