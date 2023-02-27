from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.models import User
from request.models import Request
from django.db.models import Q
from panel.models import Category
from django.db.models import Sum
import codecs
from django.http import HttpResponse
import csv
import json
# Create your views here.

class ReportView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    model = Request
    template_name = 'report.html'
    paginate_by = 10
    context_object_name = 'objects'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # all system transactions
            return Request.objects.all().order_by('id')
        else:
            # all transaction its owner or in pay_list
            return Request.objects.filter(Q(owner=self.request.user) | Q(pay_list__in=[self.request.user])).order_by('id') #here use filter

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(name__isnull=False).order_by('name')
        context['categories'] = categories
        header = ['Month']
        arr = []
        for category in categories:
            header.append(category.name)
        arr.append(header)
 
        dates = Request.objects.filter(Q(owner=self.request.user)|Q(users__in=[self.request.user])).values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
        if len(dates) > 0:
            for date in dates:
                lts = [0]* len(header)
                lts[0] = "{0}-{1}".format(date['start_at__month'],date['start_at__year'])            
                c = Request.objects.filter(start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
                for c1 in c:
                    for cat in categories:
                        if c1['category__name'] == cat.name:
                            lts[header.index(cat.name)] = float(c1['total'])
                arr.append(lts)
        else:
            lts = [0]*len(header)
            arr.append(lts)
        context['list'] = arr 
        context['users'] = User.objects.all()
        to_pay = Request.objects.filter((Q(amount__lte=self.request.user.wallet.limit) | Q(is_approved=True)) & ~Q(pay_list__in=[self.request.user]),users__in=[self.request.user],is_pay=False)
        to_approve = Request.objects.filter(is_approved=False)
        if len(to_pay) == 0 and len(to_approve) == 0:
            has_notify = False
        else:
            has_notify = True
        
        if len(to_pay) == 0:
            has_note = False
        else:
            has_note = True

        context['has_note'] = has_note
        context['has_notify'] = has_notify
        return context


def filter_user(request,user):
    
    categories = Category.objects.filter(name__isnull=False).order_by('name')
    header = ['Month']
    arr = []
    for category in categories:
        header.append(category.name)
    arr.append(header)
    if user > 0:
        dates = Request.objects.filter(Q(owner=User.objects.get(id=user).id) | Q(users__in=[User.objects.get(id=user)])).values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
    else:
        dates = Request.objects.all().values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
    if len(dates) > 0:
        for date in dates:
            lts = [0]* len(header)
            lts[0] = "{0}-{1}".format(date['start_at__month'],date['start_at__year'])     
            if user == 0:       
                c = Request.objects.filter(start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
            else:
                c = Request.objects.filter(Q(owner=user),start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
            for c1 in c:
                for cat in categories:
                    if c1['category__name'] == cat.name:
                        lts[header.index(cat.name)] = float(c1['total'])
            arr.append(lts)
    else:
        lts = [0]* len(header)
        arr.append(lts)
    return HttpResponse(json.dumps({'data':arr}))

def filter_category(request,category):
    if category > 0:
        cat = Category.objects.get(id=category)
        categories = Category.objects.filter(name = cat.name,name__isnull=False).order_by('name')
    else:
        cat = Category.objects.all()
        categories = Category.objects.all().order_by('name')
    
    header = ['Month']
    arr = []
    for category in categories:
        header.append(category.name)
    arr.append(header)

    dates = Request.objects.filter(Q(owner=request.user)|Q(users__in=[request.user])).values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
    if len(dates) >0:
        for date in dates:
            lts = [0]* len(header)
            lts[0] = "{0}-{1}".format(date['start_at__month'],date['start_at__year'])            
            c = Request.objects.filter(start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
            for c1 in c:
                for cat in categories:
                    if c1['category__name'] == cat.name:
                        lts[header.index(cat.name)] = float(c1['total'])
            arr.append(lts)
    else:
        lts = [0]* len(header)
        arr.append(lts)
    return HttpResponse(json.dumps({'data':arr}))


def filter_start(request,start):
    categories = Category.objects.filter(name__isnull=False).order_by('name')
    header = ['Month']
    arr = []
    for category in categories:
        header.append(category.name)
    arr.append(header)

    dates = Request.objects.filter(Q(owner=request.user)|Q(users__in=[request.user]),start_at__gte=start).values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
    if len(dates) > 0:
        for date in dates:
            lts = [0]* len(header)
            lts[0] = "{0}-{1}".format(date['start_at__month'],date['start_at__year'])            
            c = Request.objects.filter(start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
            for c1 in c:
                for cat in categories:
                    if c1['category__name'] == cat.name:
                        lts[header.index(cat.name)] = float(c1['total'])
            arr.append(lts)
    else:
       lts = [0]* len(header)
       arr.append(lts)
    return HttpResponse(json.dumps({'data':arr}))

def filter_end(request,end):
    categories = Category.objects.filter(name__isnull=False).order_by('name')
    header = ['Month']
    arr = []
    for category in categories:
        header.append(category.name)
    arr.append(header)

    dates = Request.objects.filter(Q(owner=request.user)|Q(users__in=[request.user]),start_at__lte=end).values('start_at__month','start_at__year').distinct().order_by('start_at__year','start_at__month')
    if len(dates) > 0:
        for date in dates:
            lts = [0]* len(header)
            lts[0] = "{0}-{1}".format(date['start_at__month'],date['start_at__year'])            
            c = Request.objects.filter(start_at__month=date['start_at__month'],start_at__year=date['start_at__year'],category__name__isnull=False).values('category__name').annotate(total=Sum('amount')).order_by('start_at__year','start_at__month','category__name')
            for c1 in c:
                for cat in categories:
                    if c1['category__name'] == cat.name:
                        lts[header.index(cat.name)] = float(c1['total'])
            arr.append(lts)
    else:
        lts = [0]* len(header)
        arr.append(lts)
    return HttpResponse(json.dumps({'data':arr}))


def download_file(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="info.csv"'},
    )
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['','','','All Transactions'])
    writer.writerow([''])
    writer.writerow(['Category', 'Owner','Date','Amount','Pay users','Participants','Note','Attachment'])
    try:
        if request.user.is_superuser:
            requests = Request.objects.all()
        else:
            requests = Request.objects.filter(Q(owner=request.user)|Q(users__in=[request.user]))
    except Request.DoesNotExist:
        requests = None
    if requests is not None:
        for request in requests:
            users = []
            pay_list = []
            if request.users.all():
                for user in request.users.all():
                    users.append(user.first_name)
            if request.pay_list.all():
                for user in request.pay_list.all():
                    pay_list.append(user.first_name)
            writer.writerow([request.category,request.owner,request.start_at,request.amount,pay_list,users,request.note,request.attachment])
            users.clear()
            pay_list.clear()
    else:
        writer.writerow(['','','','','','','',''])
    return response