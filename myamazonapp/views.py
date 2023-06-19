from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import *
# Create your views here.
from .forms import RegistrationForm , LoginForm
def home(request):
    products=Product.objects.all()
    username=str(request.user)
    return render(request,"home.html",{'products':products,'fname':username})
def signin(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if (form.is_valid()):
            name=form.cleaned_data['username']
            password1=form.cleaned_data['password']
            existing=User.objects.all()
            for users in existing:
                if(str(users)==str(name)):
                  valid_user= authenticate(username=name,password=password1)  
                  if valid_user is not None:
                    login(request,valid_user)
                    fname=valid_user.first_name
                    return redirect('home')
                  else:
                    messages.error(request,'Invalid Credentials') 
                    return render(request,'home.html',{'error_message':"Invalid Credentials"})
    return render(request,'signin.html',{'form':form })
def signup(request):
    form=RegistrationForm()
    if(request.method=='POST'):
        form=RegistrationForm(request.POST)
        if(form.is_valid()):
           name=request.POST['username']
           password=request.POST['password']
           first_name=request.POST['firstname']
           last_name=request.POST['lastname']
           myuser=User.objects.create_user(name,'',password)
           myuser.first_name= first_name
           myuser.last_name= last_name
           myuser.save()
           mycustomer=Customer.objects.create(username=myuser)
           mycustomer.save() 
           return redirect('signin')
    return render(request,'signup.html',{'form':form})
def signout(request):
    logout(request)
    return redirect('home')
def addincart(request,id):
    customer1=Customer.objects.get(username=request.user)
    if (Order.objects.filter(customer=customer1,complete=False)):
       order=Order.objects.filter(customer=customer1,complete=False)
    else:
       order=Order.objects.create(customer=customer1,date='2023-03-03',complete=False)
       order.save()
       order=Order.objects.filter(customer=customer1,complete=False)
    for i in order:
       orderobject=i
    product=Product.objects.get(id=id)
    print(product.id)
    orderitem=OrderItem.objects.create(order=orderobject,product=product,quantity=1)
    orderitem.save()
    return redirect("/home") 
def cart(request):
   error=''
   carttotal=0
   customer1=Customer.objects.get(username=request.user)
   if (Order.objects.filter(customer=customer1,complete=False)):
       order=Order.objects.get(customer=customer1,complete=False)
       items=OrderItem.objects.filter(order=order)
       carttotal=order.carttotal
   else:
       error="Nothing exist in orders "
       items=''
   j=0
   for item in items:
       j+=1
   return render(request,'cart.html',{'error':error,'items':items,'carttotal':carttotal,'totalitems':j})
def checkout(request):
    error=''
    carttotal=0
    customer1=Customer.objects.get(username=request.user)
    if (Order.objects.filter(customer=customer1,complete=False)):
       order=Order.objects.get(customer=customer1,complete=False)
       carttotal=order.carttotal
    else:
       error="Nothing exist in orders "
   
    items=OrderItem.objects.filter(order=order)
    j=0
    for item in items:
       j+=1
    return render(request,'checkout.html',{'items':items,'carttotal':carttotal,'totalitems':j})
def proceed(request):
   customer1=Customer.objects.get(username=request.user)
   order=Order.objects.get(customer=customer1,complete=False)
   amount=order.carttotal
   if request.method=="POST":
    city=request.POST['city']
    state=request.POST['state']
    zipcode=request.POST['zipcode']
    address=Address.objects.create(customer=customer1,order=order,city=city,state=state,zipcode=zipcode)
    address.save()
    return render(request,'payment.html',{'amount':amount})
   return render(request,'checkout.html')
def complete(request):
   if (request.method == 'POST'):
    customer1=Customer.objects.get(username=request.user)
    order=Order.objects.get(customer=customer1,complete=False)
    order.complete=True
    order.save()
    tid=TransactionHistory.objects.create(order=order).save()
    return redirect('home')
   return render(request,'payment.html')