from django.shortcuts import render
from .forms import RequestForm, ReversedIncomeForm, ReversedToAvailableForm
from django.contrib import messages
from core.models import Wallet
from django.http import HttpResponse
import json
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Request, PayHistory, ApproveHistory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from webpush import send_user_notification
# Create your views here.

def requests(request):
    to_pay = Request.objects.filter((Q(amount__lte=request.user.wallet.limit) | Q(is_approved=True)) & ~Q(pay_list__in=[request.user]),users__in=[request.user],is_pay=False)
    paginator = Paginator(to_pay,10)
    page = request.GET.get('page1')
    try:
        to_pay = paginator.page(page)
    except PageNotAnInteger:
        to_pay = paginator.page(1)
    except EmptyPage:
        to_pay = paginator.page(paginator.num_pages)

    to_approve = Request.objects.filter(is_approved=False)
    paginator = Paginator(to_approve,10)
    page = request.GET.get('page2')
    try:
        to_approve = paginator.page(page)
    except PageNotAnInteger:
        to_approve = paginator.page(1)
    except EmptyPage:
        to_approve = paginator.page(paginator.num_pages)
    request_form = RequestForm()
    if len(to_approve) == 0 and len(to_pay) == 0:
        has_notify = False
    else:
        has_notify = True
    context = {'to_pay':to_pay, 'to_approve':to_approve,'request_form':request_form,'has_notify':has_notify}  
    return render(request,'requests.html',context)


def add_request(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST,request.FILES)

        if request_form.is_valid():
            object = request_form.save(commit=False)
            object.owner = request.user
            
            object.request_type = 'expense'
            if request_form.cleaned_data['amount'] > request.user.wallet.limit:
                object.is_approved = False
            object.save()

            request_form.save_m2m()
            object.pay_list.add(request.user)
            object.save()
            wallet = Wallet.objects.get(user=request.user)
            wallet.available_balance -= request_form.cleaned_data['amount']
            wallet.save()

            for user in object.users.all():
                payload = {"head": "Welcome!", "body": f"Hi {user.username}, you have new request","icon":"/static/images/logo.png",'url':reverse(requests),}
                send_user_notification(user=user, payload=payload, ttl=1000)
            messages.success(request,"New Transaction is added {0}".format(request_form.cleaned_data['category']))
            return HttpResponse(
                json.dumps({"result":True})
        )

        return HttpResponse(json.dumps(
            request_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))


def add_reversed_income(request):
    if request.method == "POST":
        request_form = ReversedIncomeForm(request.POST,request.FILES)

        if request_form.is_valid():
            object = request_form.save(commit=False)
            object.owner = request.user
            object.is_pay = True
            object.save()
            users = User.objects.all()
            for user in users:
                object.users.add(user)
                object.save()
            
            # request_form.save_m2m()
            wallets = Wallet.objects.all()
            share = request_form.cleaned_data['amount'] / 100
            for wallet in wallets:
                wallet.reversed_account += (share * wallet.share_percentage)
                wallet.save()
            for user in object.users.all():
                payload = {"head": "Welcome!", "body": f"Hi {user.username}, you have new reversed income","icon":"/static/images/logo.png",'url':reverse(requests),}
                send_user_notification(user=user, payload=payload, ttl=1000)
            messages.success(request,"New Transaction is added {0}".format(request_form.cleaned_data['category']))
            return HttpResponse(
                json.dumps({"result":True})
        )

        return HttpResponse(json.dumps(
            request_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))


def add_reversed_to_available(request):
    if request.method == "POST":
        request_form = ReversedToAvailableForm(request.POST,request.FILES)

        if request_form.is_valid():
            object = request_form.save(commit=False)
            object.owner = request.user
            object.is_pay = True
            object.save()
            users = User.objects.all()
            for user in users:
                object.users.add(user)
                object.save()
            # divide the amount to all users based on thier percentage
            wallets = Wallet.objects.all()
            share = request_form.cleaned_data['amount'] / 100
            for wallet in wallets:
                wallet.reversed_account -= (share * wallet.share_percentage)
                wallet.available_balance += (share * wallet.share_percentage) - (((share * wallet.share_percentage)/100)*10)
                wallet.emergency_balance += (((share * wallet.share_percentage)/100)*10)
                wallet.save()
            for user in object.users.all():
                payload = {"head": "Welcome!", "body": f"Hi {user.username}, you have new available balance","icon":"/static/images/logo.png",'url':reverse(requests),}
                send_user_notification(user=user, payload=payload, ttl=1000)
            # wallet = Wallet
            messages.success(request,"New Transaction is added {0}".format(request_form.cleaned_data['category']))
            return HttpResponse(
                json.dumps({"result":True})
        )

        return HttpResponse(json.dumps(
            request_form.errors
            ,ensure_ascii = False)
        )
    return HttpResponse(json.dumps({"result":True}))


def review(request,id):
    instance = Request.objects.get(id=id)
    request_form = RequestForm(instance=instance)
    return HttpResponse(request_form)

def pay(request, id):
    # the request that I will pay for it
    me_request = Request.objects.get(id=id)
    wallet = Wallet.objects.get(user=request.user)
    #count number of users in the request and take from current user balance and add to the request owner balance
    wallet.available_balance -= me_request.user_amount
    wallet.save()
    # the wallet of request owner that will pay for it
    reciever_wallet = Wallet.objects.get(user=me_request.owner)
    sender = Request.objects.create(amount=me_request.user_amount,owner=request.user,note='{0} pay to {1}'.format(request.user,me_request.owner),category=me_request.category,request_type='expense',start_at=datetime.datetime.now(),is_pay=True,is_approved=True)
    sender.pay_list.add(me_request.owner)
    sender.users.add(me_request.owner)
    sender.users.add(request.user)
    sender.save()
    payload = {"head": "New pay!", "body": f"Hi {request.user.username}, you pay {me_request.user_amount} for {me_request.category}","icon":"/static/images/logo.png",'url':reverse(requests),}
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    PayHistory.objects.create(request=me_request,pay_by=request.user)
    reciever_wallet.available_balance += me_request.user_amount
    reciever_wallet.save()
    reciever = Request.objects.create(amount=me_request.user_amount,owner=me_request.owner,note="{0} recieve from {1}".format(me_request.owner,request.user),category=me_request.category,request_type='income',start_at=datetime.datetime.now(),is_pay=True,is_approved=True)
    reciever.pay_list.add(request.user)
    reciever.users.add(request.user)
    reciever.users.add(me_request.owner)
    reciever.save()
    payload = {"head": "New income!", "body": f"Hi {me_request.owner}, you recieve {me_request.user_amount} from {me_request.category}","icon":"/static/images/logo.png",'url':reverse(requests),}
    send_user_notification(user=me_request.owner, payload=payload, ttl=1000)
    me_request.pay_list.add(request.user)
    me_request.save()
    
    return HttpResponse(True)

def approve(request, id):
    me_request = Request.objects.get(id=id)
    me_request.is_approved = True
    me_request.save()
    for user in me_request.users.all():
        payload = {"head": "Approved request!","body": f"Hi {user.username}, someone approve a request","icon":"/static/images/logo.png",'url':reverse(requests),}
        send_user_notification(user=user, payload=payload, ttl=1000)
    return HttpResponse(True)