from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('about/',views.about),
    path('contactus/',views.contactus),
    path('myorders/',views.myorders),
    path('singin/',views.singin),
    path('products/',views.prod),
    path('signup/',views.signup),
    path('myprofile/',views.myprofile),
    path('viewdetails/',views.viewdetails),
    path('process/',views.process),
    path('logout/',views.logout),
    path('cart',views.cart),

    ]