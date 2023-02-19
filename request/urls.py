from django.urls import path
from .views import requests,add_request, add_reversed_income,add_reversed_to_available, review, pay, approve

urlpatterns = [
    path('',requests, name='requests'),
    path('add-request/',add_request,name="add_request"),
    path('add-reversed-income/',add_reversed_income,name="add_reversed_income"),
    path('add-reversed-to-available/', add_reversed_to_available, name='add_reversed_to_available'),
    path('review/<int:id>',review, name='review'),
    path('pay/<int:id>',pay, name='pay'),
    path('approve/<int:id>', approve, name='approve'),
]
