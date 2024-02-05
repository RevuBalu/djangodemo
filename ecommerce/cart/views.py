from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Account,Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
@login_required
def cartview(request):
    total=0
    u=request.user
    try:
       c=Cart.objects.filter(user=u)
       for i in c:
          total+=i.quantity*i.product.price
    except:
        pass
    return render(request,'cart.html',{'d':c,'t':total})
@login_required
def addtocart(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        c=Cart.objects.get(user=u,product=p)
        if (p.stock>0):
               c.quantity+=1
               c.save()
               p.stock -= 1
               p.save()
    except:
        if (p.stock>0):
            c=Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock-=1
            p.save()
    return cartview(request)
@login_required
def cart_remove(request,n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
         c = Cart.objects.get(user=u, product=p)
         if (c.quantity>1):
           c.quantity-=1
           c.save()
           p.stock += 1
           p.save()
         else:
             c.delete()
             p.stock += 1
             p.save()
    except:
        pass
    return cartview(request)
@login_required
def full_remove(request,n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
         c = Cart.objects.get(user=u, product=p)
         c.delete()
         p.stock += c.quantity
         p.save()
    except:
        pass
    return (cartview(request))


@login_required
def orderform(request):
    if (request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0 #total bill amount
        for i in c:
            total+=i.quantity*i.product.price
        try:
            ac=Account.objects.get(acctnum=n)#to retrive the acctobject
            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()
                for i in c:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()
                c.delete()
                msg="your order placed successfully"
                return render(request,'orderdetail.html',{'m':msg})
            else:
                msg="insufficient amount.you can't place order"
                return render(request,'orderdetail.html',{'m':msg})


        except:
            pass
    return render(request,'orderform.html')
@login_required
def orderview(request):
    u=request.user
    f=Order.objects.filter(user=u)

    return render(request,'orderview.html',{'o':f,'u':u.username})

