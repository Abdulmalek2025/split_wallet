from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from panel.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

# every user has available_balance, emergency_balance, reversed_account, share_percentage, limit
# ModelName.objects.filter(field_name__isnull=True).aggregate(Sum('field_name'))


class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    available_balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    reversed_account = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    share_percentage = models.DecimalField(max_digits=7,decimal_places=5,validators=[MinValueValidator(1),MaxValueValidator(100)])
    limit = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    emergency_balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    emergency_percentage = models.DecimalField(max_digits=5,decimal_places=3,validators=[MinValueValidator(1),MaxValueValidator(100)],default=10)
    category_list = models.ManyToManyField(Category,related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_available(self):
        value = Wallet.objects.all().aggregate(total=Sum('available_balance'))
        return value['total']
    
    @property
    def total_reverce(self):
        value = Wallet.objects.all().aggregate(total=Sum('reversed_account'))
        return value['total']
    
    @property
    def total_emergency(self):
        value = Wallet.objects.all().aggregate(total=Sum('emergency_balance'))
        return value['total']
    
    @property
    def total_percentage(self):
        value = Wallet.objects.all().aggregate(total=Sum('share_percentage'))
        return value['total']
    
    @property
    def total_limit(self):
        value = Wallet.objects.all().aggregate(total=Sum('limit'))
        return value['total']
    
    def clean(self):
        wallets = Wallet.objects.all()
        print(self.share_percentage)
        if self.pk:
            value = wallets.exclude(pk=self.pk).aggregate(total=Sum('share_percentage'))
           
            if value['total'] is not None:
                print('update')
                if value['total']+self.share_percentage > 100:
                    raise ValidationError({'share_percentage':"Use less value"})
            
        else:
            value = wallets.aggregate(total=Sum('share_percentage'))
            print('create')
            if value['total'] is not None and self.share_percentage is not None:
                if value['total']+self.share_percentage > 100:
                    raise ValidationError({'share_percentage':"Use less value"})
            else:
                raise ValidationError({'share_percentage':"This field is required"})
        super(Wallet, self).clean()
