from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name=models.CharField(max_length=20)
    type=models.CharField(max_length=30)
    breed=models.CharField(max_length=30)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    description=models.CharField(max_length=300)
    price=models.IntegerField()
    pimage=models.ImageField(upload_to='image',default=0)
    
class Cart(models.Model):
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity=models.IntegerField(default=1)

class Order(models.Model):
    orderid=models.IntegerField()
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity=models.IntegerField()