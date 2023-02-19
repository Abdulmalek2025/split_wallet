from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Category
        fields = ('name',)