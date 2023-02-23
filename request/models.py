from django.db import models
from django.contrib.auth.models import User
from panel.models import Category

# Create your models here.

class Request(models.Model):
    users = models.ManyToManyField(User,related_name='all_requests')
    category = models.ForeignKey(Category, related_name='requests',blank=True,null=True,on_delete=models.SET_NULL)
    start_at = models.DateField()
    is_approved = models.BooleanField(default=True)
    is_pay = models.BooleanField(default=False)
    pay_list = models.ManyToManyField(User,related_name='pay_list')
    amount = models.DecimalField(decimal_places=2,max_digits=10)
    attachment = models.FileField(upload_to='requests/', blank=True, null=True)
    note = models.CharField(max_length=500,blank=True,null=True)
    approved_list = models.ManyToManyField(User,related_name='approves')
    owner = models.ForeignKey(User,related_name='requests',on_delete=models.PROTECT)
    is_main = models.BooleanField(default=False)
    request_type = models.CharField(max_length=50,blank=True,null=True,default='expense')
    created_at = models.DateField(auto_now_add=True)


    @property
    def user_amount(self):
        return (self.amount / self.users.all().count())
    


class ApproveHistory(models.Model):
    request = models.ForeignKey(Request,related_name='approves',on_delete=models.PROTECT)
    approved_by = models.ForeignKey(User,on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)

class PayHistory(models.Model):
    request = models.ForeignKey(Request,related_name="pays", on_delete=models.PROTECT)
    pay_by = models.ForeignKey(User,on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)