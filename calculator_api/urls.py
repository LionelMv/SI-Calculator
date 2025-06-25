from django.urls import path
from .views import CalculateView, InstrumentListView

urlpatterns = [
    path('calculate/', CalculateView.as_view(), name='calculate'),
    path('instruments/', InstrumentListView.as_view(), name='instruments'),
]
