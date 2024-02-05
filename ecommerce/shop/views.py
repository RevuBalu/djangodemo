from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
def allcategories(request):
    t=Category.objects.all()
    return render(request,'category.html',{'p':t})
def categorydetail(request,p):
    d=Category.objects.get(name=p)
    p=Product.objects.filter(category=d)
    return render(request,'categorydetail.html',{'m':d,'c':p})
def productdetail(request,p):
    p=Product.objects.get(name=p)
    return render(request,'productdetail.html',{'h':p})
def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        c=request.POST['c']
        e=request.POST['e']
        f=request.POST['f']
        l=request.POST['l']

        if (p==c):
            r=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l,)
            r.save()
            return redirect('shop:allcategories')

        else:
            return HttpResponse("Passwords are not same")

    return render(request,'register.html')
def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        l=authenticate(username=u,password=p)
        if l:
            login(request,l)
            return redirect('shop:allcategories')
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'login.html')
@login_required
def user_logout(request):
    logout(request)
    return render(request,'login.html')
