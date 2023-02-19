import json
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from account.forms import SignUpForm, EditForm, SetPasswordForm
from core.forms import WalletForm
from django.contrib.auth.models import User
from .models import Category
from .forms import CategoryForm
# Create your views here.

def panel(request):
    signup_form = SignUpForm()
    password_change_form = SetPasswordForm(request.user)
    wallet_form = WalletForm()
    edit_form = EditForm()
    category_form = CategoryForm()
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
    return render(request,'admin_panel.html', context={'signup_form':signup_form,'wallet_form':wallet_form,'edit_form':edit_form,'password_change':password_change_form,'category_form':category_form,'users':users,'categories':categories})


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