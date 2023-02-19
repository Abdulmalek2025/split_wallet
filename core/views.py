from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from panel.models import Category
from core.models import Wallet
from request.models import Request
from request.forms import RequestForm,ReversedIncomeForm, ReversedToAvailableForm
from django.contrib import messages
import json
import datetime
from django.db.models import Sum
# Create your views here.


class IndexView(LoginRequiredMixin, ListView):
    # login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Request
    template_name = 'index.html'
    paginate_by = 10
    context_object_name = 'objects'

    def get_queryset(self):
        return Request.objects.filter(owner=self.request.user).order_by('-id') #here use filter

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['request_form'] = RequestForm()
        context['request_form'].fields['category'].queryset = Category.objects.filter(visible=True)
        context['reversed_income_form'] = ReversedIncomeForm()
        income, in_created = Category.objects.get_or_create(name='Reserved Income to shareholders',visible=False)
        context['reversed_income_form'].fields['category'].queryset = Category.objects.filter(name="Reserved Income to shareholders")
        context['reversed_to_available_form'] = ReversedToAvailableForm()
        expense, ex_created = Category.objects.get_or_create(name='Reversed Available to shareholder',visible=False)
        context['reversed_to_available_form'].fields['category'].queryset = Category.objects.filter(name="Reversed Available to shareholder")
        today = datetime.datetime.now()
        context['month_income'] =  Request.objects.filter(start_at__month=today.month, request_type='income').aggregate(Sum('amount'))
        context['month_expense'] = Request.objects.filter(start_at__month=today.month, request_type='expense').aggregate(Sum('amount'))
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        
        return context
    



