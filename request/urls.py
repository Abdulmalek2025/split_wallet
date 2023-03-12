from django.urls import path
from .views import requests,add_request, add_reversed_income,add_reversed_to_available,\
      review, pay, approve, edit_approve,add_emergency_to_available, complete,reject,admin_request

urlpatterns = [
    path('',requests, name='requests'),
    path('add-request/',add_request,name="add_request"),
    path('add-reversed-income/',add_reversed_income,name="add_reversed_income"),
    path('add-reversed-to-available/', add_reversed_to_available, name='add_reversed_to_available'),
    path('add-emergency-to-available/',add_emergency_to_available,name='add_emergency_to_available'),
    path('review/<int:id>',review, name='review'),
    path('pay/<int:id>',pay, name='pay'),
    path('approve/<int:id>', approve, name='approve'),
    path('edit-approve-list/<int:id>/',edit_approve, name="edit_approve"),
    path('complete/<int:id>/',complete, name='complete'),
    path('reject/<int:id>/',reject,name='reject'),
    path('admin-request/',admin_request, name="admin_request")
]
