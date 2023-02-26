from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm,SetPasswordForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    is_staff = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'is_superuser', 'is_staff')


class LoginForm(AuthenticationForm):
    username = username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    remember_me = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

    class Meta:
        model = User
        fields = ('username','password','remember_me')


class EditForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # is_superuser = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    is_staff = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'is_staff')


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']