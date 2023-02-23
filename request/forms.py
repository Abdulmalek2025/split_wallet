from django import forms
from django.contrib.auth.models import User
from .models import Request
from panel.models import Category

class RequestForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select'}))
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple)
    start_at = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    attachment = forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Request
        fields = ('category','users','start_at','amount','attachment','note')

class ReversedIncomeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select'}),empty_label=None)
    start_at = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    attachment = forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Request
        fields = ('category','start_at','amount','attachment','note')


class ReversedToAvailableForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select'}),empty_label=None)
    start_at = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    attachment = forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Request
        fields = ('category','start_at','amount','attachment','note')


class ApproveForm(forms.ModelForm):
    approved_list = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple)
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','readonly':True}))

    class Meta:
        model = Request
        fields = ('id','amount','approved_list','users')