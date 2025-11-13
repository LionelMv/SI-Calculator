from django.shortcuts import render
from rest_framework.request import Request
from django.http import HttpResponse
# from calculator_api.constants import CHOICES, INSTRUMENTS


# def index(request):
#     instruments_map = {choice[1]: INSTRUMENTS.get(choice[0])
#                     for choice in CHOICES}

#     return render(request, 'frontend_ui/index.html', {
#         'instruments': CHOICES,
#         'instruments_map': instruments_map
#     })

def index(request: Request) -> HttpResponse:
    return render(request, 'frontend_ui/index.html')
