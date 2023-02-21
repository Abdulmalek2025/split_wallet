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
from django.db.models import Sum,Q
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
        context['request_form'] = RequestForm(initial={'users': [self.request.user.id]})
        context['request_form'].fields['category'].queryset = Category.objects.filter(visible=True)
        context['reversed_income_form'] = ReversedIncomeForm()
        income, in_created = Category.objects.get_or_create(name='Reserved Income to shareholders',visible=False)
        context['reversed_income_form'].fields['category'].queryset = Category.objects.filter(name="Reserved Income to shareholders")
        context['reversed_to_available_form'] = ReversedToAvailableForm()
        expense, ex_created = Category.objects.get_or_create(name='Reversed Available to shareholder',visible=False)
        context['reversed_to_available_form'].fields['category'].queryset = Category.objects.filter(name="Reversed Available to shareholder")
        today = datetime.datetime.now()
        context['month_income'] =  Request.objects.filter(start_at__month=today.month, request_type='income',owner=self.request.user).aggregate(Sum('amount'))
        context['month_expense'] = Request.objects.filter(start_at__month=today.month, request_type='expense',owner=self.request.user).aggregate(Sum('amount'))
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        to_pay = Request.objects.filter((Q(amount__lte=self.request.user.wallet.limit) | Q(is_approved=True)) & ~Q(pay_list__in=[self.request.user]),users__in=[self.request.user],is_pay=False)
        to_approve = Request.objects.filter(is_approved=False)
        if len(to_pay) == 0 and len(to_approve) == 0:
            has_notify = False
        else:
            has_notify = True
        context['has_notify'] = has_notify
        return context
    



