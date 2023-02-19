from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,related_name='categories',null=True, blank=True, on_delete=models.SET_NULL,)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def monthly_amount(self):
        return (Category.objects.filter(name=self.name).values('requests__start_at__month','requests__start_at__year','name').annotate(total=models.Sum('requests__amount')).order_by('requests__start_at__month'))

    def __str__(self):
        return self.name
    