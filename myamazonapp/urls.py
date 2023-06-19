from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('signout',views.signout,name="signout"),
    path('addincart/<int:id>',views.addincart),
    # path('product/<int:id>',views.product),
    path('cart',views.cart),
    path('checkout',views.checkout),
    path('proceed',views.proceed),
    path('complete',views.complete),

]