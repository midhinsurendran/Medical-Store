from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    author =  models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    medicine = models.CharField(max_length=500)
    stock = models.DecimalField(max_digits=10,decimal_places=0)
    time=models.DateTimeField(auto_now=True)