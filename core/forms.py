from django import forms
from django.core import validators
from panel.models import Category
from .models import Wallet

class WalletForm(forms.ModelForm):
    available_balance = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class':'form-control'}))
    reversed_account = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class':'formcontrol'}))
    share_percentage = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    limit = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    category_list = forms.ModelMultipleChoiceField(required=False,queryset=Category.objects.filter(visible=True),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Wallet
        fields = ('available_balance','reversed_account', 'share_percentage', 'limit', 'category_list')

class EmergencyForm(forms.ModelForm):
    emergency_percentage = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Wallet
        fields = ('emergency_percentage',)

class EmergencyPerForm(forms.Form):
    emergency_percentage = forms.DecimalField(required=True,validators=[validators.MinValueValidator(1),validators.MaxValueValidator(100)],widget=forms.NumberInput(attrs={'class':'form-control'}))
