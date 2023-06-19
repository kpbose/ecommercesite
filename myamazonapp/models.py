from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
       username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class Product(models.Model):
    name=models.CharField(max_length=30)
    category=models.CharField(max_length=30)
    price=models.IntegerField(max_length=30)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    date=models.DateField()
    
    @property
    def carttotal(self):
         items=self.orderitem_set.all()
         total=sum([item.itemtotal for item in items])
         return total
    def totalitems(self):
         items=self.orderitem_set.all()
         i=0
         for i in items:
              i+=1
         return i
class OrderItem(models.Model):
     product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
     order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
     quantity=models.IntegerField()
    
     @property
     def itemtotal(self):
          return self.product.price*self.quantity
class Address(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.IntegerField(null=True)
    date_added=models.DateTimeField(auto_now_add=True)

class TransactionHistory(models.Model):
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    TransactionId=models.CharField(max_length=30)
    
