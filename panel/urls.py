from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from .views import panel, add_category,edit_category,delete_category,edit_emergency, edit_request, print

urlpatterns = [
    path('',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(panel), name='panel'),
    path('add-category/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(add_category), name='add_category'),
    path('edit-category/<int:id>/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(edit_category), name='edit_category'),
    path('edit-emergency/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(edit_emergency), name='edit_emergency'),
    path('delete/<int:id>/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(delete_category), name='delete_category'),
    path('edit-request/<int:id>/', user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(edit_request),name='edit_request'),
    path('print-request/<int:id>/',user_passes_test(lambda u:u.is_superuser, login_url='/accounts/login')(print), name='print'),
]
