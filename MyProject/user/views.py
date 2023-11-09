from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import datetime
from django.db import connection


# Create your views here.
def home(req):

    cdata=category.objects.all().order_by('-id')[0:6]
    pdata=products.objects.all().order_by('-id')[0:12]
    print(pdata)

    return render(req,'user/index.html',{"data":cdata,"prod":pdata})

def about(req):
    return render(req,'user/about.html')

def contactus(request):
    status=False
    if request.method=='POST':
        a=request.POST.get("name","")
        b=request.POST.get("mobile","")
        c=request.POST.get("email","")
        d=request.POST.get("msg","")
        x=contact(name=a,email=c,contact=b,message=d)
        x.save()
        status=True
    return render(request,'user/contactus.html',{'S':status})

def myprofile(request):
    user=request.session.get('userid')
    pdata=profile.objects.filter(email=user)
    if user:
        if request.method == 'POST':
            name = request.POST.get("name", "")
            DOB = request.POST.get("dob", "")
            Mobile = request.POST.get("mobile", "")
            Password = request.POST.get("passwd", "")
            ProfilePhoto = request.FILES['myfile']
            Address = request.POST.get("address", "")
            profile(email=user,name=name,dob=DOB,passwd=Password,mobile=Mobile,myfile=ProfilePhoto,address=Address).save()
            return HttpResponse("<script>alert('Your Profile updated Successfully..');window.location.href='/user/myprofile/'</script>")



    return render(request,'user/myprofile.html',{"profile":pdata})

def myorders(request):
    userid=request.session.get('userid')
    oid=request.GET.get('oid')
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o,user_products p where o.pid=p.id and o.userid='"+str(userid)+"'")
        orderdata=cursor.fetchall()
        if oid:
            result=order.objects.filter(id=oid,userid=userid)
            result.delete()
            return HttpResponse("<script>alert('Your order has been cancelled...')window.location.href='/user/myorders'</script>")

    return render(request,'user/myorders.html',{"pendingorder":orderdata})

def singin(request):
    if request.method=='POST':
        uname=request.POST.get('email',"")
        pwd=request.POST.get('passwd',"")
        checkuser=profile.objects.filter(email=uname,passwd=pwd)
        #print(checkuser)
        if(checkuser):
            request.session['userid']=uname
            return HttpResponse("<script>alert('LoogedIn sucessfully');window.location.href='/user/singin/';</script>")
        else:
            return HttpResponse("<script>alert('UserId or Password is incorrect');window.location.href='/user/singin/';</script>")

    return render(request,'user/singin.html')

def prod(request):
    cdata=category.objects.all().order_by('-id')
    x=request.GET.get('abc')
    pdata=""
    if x is not None:
        pdata=products.objects.filter(category=x)
    else:
        pdata = products.objects.all().order_by('-id')


    return render(request,'user/product.html',{"cat":cdata,"products":pdata})

def signup(request):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Password = request.POST.get("passwd", "")
        Address = request.POST.get("address", "")
        Picname = request.FILES['fu']
        # profile(name=name,mobile=mobile,email=email,passwd=password,address=address,ppic=picname).save()
        # return HttpResponse("<script>alert('you are Registerd successfully..');window.location.href='/user/signup';</script>")
        d = profile.objects.filter(email=Email)

        if d.count() > 0:
            return HttpResponse(
                "<script>alert('Your  Allready Register...');window.location.href='/user/signup';</script>")
        else:
            profile(name=Name, mobile=Mobile, email=Email, passwd=Password, address=Address, ppic=Picname).save()
            return HttpResponse(
                "<script>alert('You Register successful..');window.location.href='/user/signup';</script>")

    return render(request, 'user/signup.html')

def viewdetails(request):
    a=request.GET.get('msg')
    data=products.objects.filter(id=a)

    return render(request,'user/viewdetails.html',{"d":data})

def process(request):
    userid=request.session.get('userid')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    print(userid,pid,btn)
    if userid is not None:
        if btn=='cart':
            checkcartitem=addtocart.objects.filter(pid=pid,userid=userid)
            if checkcartitem.count()==0:
                addtocart(pid=pid,userid=userid,status=True,cdate=datetime.datetime.now()).save()
            else:return HttpResponse("<script>alert('This items is already added in cart...');window.location.href='/user/home/'</script>")
        elif btn=='order':
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your order have comfirmed...');window.location.href='/user/myorders/'</script>")

        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your order have comfirmed...');window.location.href='/user/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True})

    else:
        return HttpResponse("<script>window.location.href='/user/singin/'</script>")

def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")

def cart(request):
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_products p where p.id=c.pid and userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()
        pid=request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(id=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('Your product has been removed successfully');window.location.href='/user/cart'</script>")
        

    return render(request,'user/cart.html',{"cart":cartdata})



