from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from .views import panel, add_category,edit_category,delete_category

urlpatterns = [
    path('',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(panel), name='panel'),
    path('add-category/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(add_category), name='add_category'),
    path('edit-category/<int:id>/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(edit_category), name='edit_category'),
    path('delete/<int:id>/',user_passes_test(lambda u:u.is_superuser,login_url='/accounts/login')(delete_category), name='delete_category')
]
