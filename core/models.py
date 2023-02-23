from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

# every user has available_balance, emergency_balance, reversed_account, share_percentage, limit
# ModelName.objects.filter(field_name__isnull=True).aggregate(Sum('field_name'))

# def check_percentage(value):
#     percentage = Wallet.objects.all().aggregate(Sum('share_percentage'))
#     if percentage is not None:
#         percentage['share_percentage__sum'] += value
#         if percentage['share_percentage__sum'] < 100 or percentage['share_percentage__sum'] == 100:
#             return value
#         else:
#             raise ValidationError('Use less value')
#     else:
#         return value

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    available_balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    reversed_account = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    share_percentage = models.DecimalField(max_digits=3,decimal_places=1,validators=[MinValueValidator(1),MaxValueValidator(100)])
    limit = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    emergency_balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        wallets = Wallet.objects.all()
        print(self.share_percentage)
        if self.pk:
            value = wallets.exclude(pk=self.pk).aggregate(total=Sum('share_percentage'))
            print("has",value['total'])
            if value['total']+self.share_percentage > 100:
                
                raise ValidationError({'share_percentage':"Use less value"})
        else:
            value = wallets.aggregate(total=Sum('share_percentage'))
            print(value['total'])
            if value['total'] + self.share_percentage > 100:
                raise ValidationError({'share_percentage':"Use less value"})
        super(Wallet, self).clean()
