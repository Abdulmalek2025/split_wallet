from django.urls import path
from django.contrib.auth.views import (LogoutView, 
                                        PasswordChangeView, PasswordChangeDoneView,
                                        PasswordResetView,PasswordResetDoneView,
                                        PasswordResetConfirmView,
                                        PasswordResetCompleteView)
from .views import Login, create_user,edit_user, delete_user,change_password


app_name = 'account'

urlpatterns = [
    path('register/',create_user, name='register'),
    path('edit/<int:id>/',edit_user,name='edit'),
    path('delete/<int:id>/',delete_user, name='delete'),
    path('change_password/<int:id>/', change_password, name="change_password"),
    path('login/',Login.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password_change/',PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',PasswordChangeDoneView.as_view(),name='password_change_done'),
    #reset password
    path('password_reset/',PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # path('activate/<uidb64>/<token>',activate_user,name='activate')
]
