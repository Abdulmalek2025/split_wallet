from django.urls import path
from .views import panel, add_category,edit_category,delete_category

urlpatterns = [
    path('',panel, name='panel'),
    path('add-category/',add_category, name='add_category'),
    path('edit-category/<int:id>/',edit_category, name='edit_category'),
    path('delete/<int:id>/',delete_category, name='delete_category')
]
