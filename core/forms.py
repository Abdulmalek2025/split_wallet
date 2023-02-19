from django import forms
from .models import Wallet

class WalletForm(forms.ModelForm):
    available_balance = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class':'form-control'}))
    reversed_account = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class':'formcontrol'}))
    share_percentage = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    limit = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Wallet
        fields = ('available_balance','reversed_account', 'share_percentage', 'limit')

