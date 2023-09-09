from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,JsonResponse
from .models import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import requests
import os
import time
import pandas as pd
import re
import json
# Create your views here.
from .forms import RegistrationForm , LoginForm
def home(request):
    products=Product.objects.filter(id__lt=10)
    r1=Reviews.objects.all()
    return render(request,"site.html",{'products':products,'r1':r1})
def signin(request):
    form=LoginForm()
    error_message=''
    if request.method=='POST':
        error_message='Invalid Credentials'
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
    return render(request,'signin.html',{'form':form,'error_message':error_message})
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
        else:
            return render(request,'signup.html',{'form':form})       
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
    card_no=request.POST['card_no']
    expiry=request.POST['expiry']
    cvv_no=request.POST['cvv_no']
    order.save()
    tid=TransactionHistory.objects.create(order=order,customer=customer1,cardnumber=card_no,expiry=expiry,cvv_no=cvv_no).save()
    
    return redirect('home')
   return render(request,'payment.html')
def search(request):
    if (request.method=="POST"):
       searchby=request.POST['search']
       products=Product.objects.all()
       searched=[]
       for product in products:
           if (searchby.lower() == product.name.lower()) or (searchby.lower() == product.category.lower()):
               searched.append(product)
       print(searched)
       return render(request,'search.html',{'searched':searched})
    return render(request,'search.html')
def convert_num(s):
  temp=s.split(',')
  string=''   
  for i in temp:
     string+=i
  return str(string)
def scraping(categori,pages):
 productname=[]
 p_price=[]
 category=[]
 img_urls=[]
 s=Service("C:/Download/chromedriver.exe")
 driver=webdriver.Chrome(service=s)
 driver.get("https://www.amazon.in/")
 time.sleep(2)
 search=driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
 search.send_keys(categori)
 time.sleep(1)
 search.send_keys(Keys.ENTER)
 time.sleep(2)
 soup=BeautifulSoup(driver.page_source,"lxml")
 for j in range(0,int(pages)):
  names=soup.find('div',class_="sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16")
  name=names.find_all('div',class_="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right")
  for item in name:
   element=item.find('div',class_="a-section a-spacing-small a-spacing-top-small")
   ele=element.find('h2',class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")
   e=ele.find('span',class_="a-size-medium a-color-base a-text-normal")
   productname.append(e.text)
   ele=element.find('div',class_="a-row a-size-base a-color-base")
   price=ele.find('span',class_="a-offscreen")
   p_price.append(price.text)
   category.append(categori)
  image_name=names.find_all('div',class_="sg-col sg-col-4-of-12 sg-col-4-of-16 sg-col-4-of-20 sg-col-4-of-24 s-list-col-left")
  i=1
  for image in image_name:
   imgtag=image.find('img',class_="s-image")
   img_url=imgtag.attrs['src']
   filename=categori+'_'+str(j)+'_'+str(i)
   img_file=open(filename+'.jpeg','wb')
   img_urls.append(filename+'.jpeg')
   img_file.write(urllib.request.urlopen(img_url).read())
   img_file.close()
   os.rename(f"C:/Django/amazonclone/{img_urls[-1]}", f"C:/Django/amazonclone/static/images/{img_urls[-1]}")
   i+=1
  names=soup.find('div',class_="a-section a-text-center s-pagination-container")
  name=soup.find('a',class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
  exist=name.attrs['href']
  url="https://www.amazon.in"
  new_url=url+exist
  print(new_url)
  driver.get(new_url)
  time.sleep(2)
  soup=BeautifulSoup(driver.page_source,"lxml")

 dictionary={
  'names':productname,
  'price':p_price,
  'category':category,
  'image':img_urls,
 }

 df=pd.DataFrame(dictionary,columns=['names','price','category','image'])
 df['price']=df['price'].apply(lambda x: x[1:])
 df['price']=df['price'].apply(convert_num)
 return df

def scrap(request):
    if request.method=="POST":
        category=request.POST['category']
        pages=request.POST['pages']
        df=scraping(category,pages)
        print(df)
        names=df['names']
        prices=df['price']
        categories=df['category']
        image_url=df['image']
        for i in range(0,len(names)):
          p=Product.objects.create(name=names[i],price=prices[i],category=categories[i],image=image_url[i])
          p.save()
        return render(request,"items.html",{'category':category,'pages':pages})
    return render(request,"items.html")
def services(request):  
   return render(request,"services.html")
def reviews(request):
    r1=Reviews.objects.all()
    if request.method=="POST":
      name=request.POST['name']
      review=request.POST['review']
      submitted="Submitted successfully"
      r=Reviews.objects.create(username=request.user,name=name,review=review)
      r.save()
    
      return render(request,"reviews.html",{'submitted':submitted,'r1':r1})
    return render(request,"reviews.html",{'r1':r1})
def contact(request):
   if request.method=="POST":
      name=request.POST['name']
      email=request.POST['email']
      subject=request.POST['subject']
      query=request.POST['query']
      submitted="Submitted Successfully"
      Query.objects.create(username=request.user,name=name,email=email,subject=subject,queri=query).save()
      return render(request,"contact.html",{'submitted':submitted})
   return render(request,"contact.html")
def products(request):
    product=Product.objects.all()
    print(product)
    return render(request,"product.html",{'product':product})