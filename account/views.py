import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, SignUpForm, EditForm, SetPasswordForm
from core.forms import WalletForm
from core.models import Wallet
from django.contrib.auth.models import User
from .utils import DecimalEncoder

class Login(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        remembrt_me = form.cleaned_data['remember_me']
        if not remembrt_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(Login, self).form_valid(form)


def create_user(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        wallet_form = WalletForm(request.POST)
        if signup_form.is_valid() and wallet_form.is_valid():
            user = signup_form.save()
            wallet = wallet_form.save(commit=False)
            wallet.user = user
            wallet.save()
            wallet_form.save_m2m()
            
            
            # Wallet.objects.create(limit=wallet_form.cleaned_data['limit'],share_percentage=wallet_form.cleaned_data['share_percentage'],user=user)
            messages.success(request,"New user is added successfully '{0}'".format(signup_form.cleaned_data['username']))
            return HttpResponse(
                json.dumps({"result":True})
        )
        errors = {**signup_form.errors,**wallet_form.errors}
        return HttpResponse(json.dumps(
            errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))


def edit_user(request,id):
    try:
        user = User.objects.get(id = id)
        wallet = Wallet.objects.get(user=user)
        user_form = EditForm(instance=user)
        wallet_form = WalletForm(instance=wallet)
    except Exception as e: 
        # messages.error(request, e.message)
        return redirect('panel')
    if request.method == 'POST':
     
        user_form = EditForm(request.POST,instance=user)
        wallet_form = WalletForm(request.POST,instance=wallet)
        if user_form.is_valid() and wallet_form.is_valid():
            user.username = user_form.cleaned_data['username']
            user.first_name = user_form.cleaned_data['first_name']
             
            user.is_staff = user_form.cleaned_data['is_staff']

            user.save()
            wallet.share_percentage = wallet_form.cleaned_data['share_percentage']
            wallet.limit = wallet_form.cleaned_data['limit']
            wallet.category_list.set(wallet_form.cleaned_data['category_list'])
            wallet.save()

            messages.success(request,"Update '{0}' user info successfully".format(user_form.cleaned_data['username']))
            return HttpResponse(
                json.dumps({"result":True})
        )
        errors = {**user_form.errors, **wallet_form.errors}
        return HttpResponse(json.dumps(
            errors
            ,ensure_ascii = False)
        )
    id_input = '<input type="hidden" id="user_id" name="user_id" value="'+str(id)+'">'
    return HttpResponse([user_form,wallet_form,id_input])


def edit_admin(request,id):
    try:
        user = User.objects.get(id = id)
        
    except Exception as e: 
        # messages.error(request, e.message)
        return redirect('panel')
    if request.method == 'POST':
     
        user_form = EditForm(request.POST,instance=user)

        if user_form.is_valid():
            user.username = user_form.cleaned_data['username']
            user.first_name = user_form.cleaned_data['first_name']
            user.is_staff = True

            user.save()

            messages.success(request,"Update '{0}' user info successfully".format(user_form.cleaned_data['username']))
            return HttpResponse(
                json.dumps({"result":True})
        )
        
        return HttpResponse(json.dumps(
            user_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps(
        {'id':user.id,'username':user.username,'first_name':user.first_name},
        ensure_ascii=False,cls= DecimalEncoder
    ))


def delete_user(request,id):
    user = User.objects.get(id=id)
    user_name = user.username
    try:
        user.delete()
        messages.success(request,"Succesfully {0} is deleted".format(user_name))
        return redirect('panel')
    except Exception as e:
        messages.error(request,e)
        return redirect('panel')
    

def change_password(request,id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        signup_form = SetPasswordForm(user,request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            messages.success(request,"New user is added successfully '{0}'".format(user.username))
            return HttpResponse(
                json.dumps({"result":True})
        )
        
        return HttpResponse(json.dumps(
            signup_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))
