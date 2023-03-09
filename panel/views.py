import json
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from account.forms import SignUpForm, EditForm, SetPasswordForm
from core.forms import WalletForm,EmergencyPerForm
from core.models import Wallet
from account.utils import DecimalEncoder
from request.models import Request
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Category
from .forms import CategoryForm
# Create your views here.



def panel(request):
    signup_form = SignUpForm()
    password_change_form = SetPasswordForm(request.user)
    wallet_form = WalletForm()
    edit_form = EditForm()
    category_form = CategoryForm()
    emergency_form = EmergencyPerForm()
    users = User.objects.all().order_by('id')
    paginator = Paginator(users,10)
    page = request.GET.get('page1')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    categories = Category.objects.all().order_by('id')
    paginator = Paginator(categories,10)
    page = request.GET.get('page2')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    transactions = Request.objects.filter(request_type='Pending').order_by('id')
    paginator = Paginator(transactions,10)
    page = request.GET.get('page3')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    
    emergency = Wallet.objects.last()
    

    to_pay = Request.objects.filter((Q(amount__lte=request.user.wallet.limit) | Q(is_approved=True)) & ~Q(pay_list__in=[request.user]),users__in=[request.user],is_pay=False)
    to_approve = Request.objects.filter(is_approved=False)
    if len(to_pay) == 0 and len(to_approve) == 0:
        has_notify = False
    else:
        has_notify = True
    return render(request,'admin_panel.html', context={'signup_form':signup_form,'wallet_form':wallet_form,'edit_form':edit_form,'password_change':password_change_form,'category_form':category_form,'users':users,'categories':categories,'emergency_form':emergency_form,'emergency':emergency,'objects':transactions,'has_notify':has_notify})


def add_category(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():

            Category.objects.create(name=category_form.cleaned_data['name'],created_by=request.user)
            
            messages.success(request,"New category is added {0}".format(category_form.cleaned_data['name']))
            return HttpResponse(
                json.dumps({"result":True})
        )
    
        return HttpResponse(json.dumps(
            category_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))


def edit_category(request,id):
    try:
        category = Category.objects.get(id = id)
    except Exception as e: 
        # messages.error(request, e.message)
        return redirect('panel')
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category.name = category_form.cleaned_data['name']
            category.save()
            
            messages.success(request,"Successfully updated category {0}".format(category_form.cleaned_data['name']))
            return HttpResponse(
                json.dumps({"result":True})
        )
        
        return HttpResponse(json.dumps(
            category_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps(
        {'id':category.id,'name':category.name},ensure_ascii=False))

def edit_emergency(request):
    try:
        emergency = Wallet.objects.last()
    except Exception as e: 
        # messages.error(request, e.message)
        return redirect('panel')
    if request.method == 'POST':
        category_form = EmergencyPerForm(request.POST)
        if category_form.is_valid():
            wallets = Wallet.objects.all().exclude(user__is_superuser=True)
            for wallet in wallets:
                wallet.emergency_percentage = category_form.cleaned_data['emergency_percentage']
                wallet.save()
            
            return HttpResponse(
                json.dumps({"result":True})
        )
        
        return HttpResponse(json.dumps(
            category_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps(
        {'emergency_percentage':emergency.emergency_percentage},ensure_ascii=False,cls=DecimalEncoder))


def delete_category(request,id):
    category = Category.objects.get(id=id)
    category_name = category.name
    try:
        category.delete()
        messages.success(request,"Succesfully {0} is deleted".format(category_name))
        return redirect('panel')
    except Exception as e:
        messages.error(request,e)
        return redirect('panel')