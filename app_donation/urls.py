from django.urls import path
from .views import *

app_name = 'app_donation'

urlpatterns = [
    path('search_rc/', search_rc, name="search_rc"),
    path('customer_service/<id>/', customer_service, name="customer_service"),
    path('confirm_ca/<id>/', confirm_ca, name='confirm_ca'),
    path('donation/<id>/', donation, name="donation"),
    path('confirm_donation/<id>', confirm_donation, name="confirm_donation"),
    path('edit_donation/<id>/', edit_donation, name="edit_donation")
]
