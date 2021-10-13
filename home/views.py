from django.shortcuts import render
from . models import *
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}



# Create your views here.
def index(request):
    Featured=Products.objects.filter(Featured=True)
    return render(request,'index.html',{'featured':Featured})


@login_required(login_url='Login')
def product(request,id):
    Product=Products.objects.get(id=id)
    return render(request,'product.html',{'product':Product})

def contact(request):
    return render(request,'contact.html')


def remove(request):
    if request.method == 'POST':
        iiid=request.POST.get('id')
        iid=iiid[1:]
        print('IID VAlue::'+str(iid))

        menuInst=Products.objects.get(id=int(iid))
        if Cart.objects.filter(user=request.user).filter(ItemID=menuInst).exists():
            x=Cart.objects.filter(user=request.user).get(ItemID=menuInst)
            try:
                if x.Quantity == 1:
                    x.delete()
                else:
                    x.Quantity=x.Quantity-1
                    x.save()
            except:
                pass
        else:
            x=Cart(user=request.user,ItemID=menuInst,Quantity=1)
            x.save()
    return JsonResponse({'res':'ok'})

@login_required(login_url='Login')
def addToCart(request):
    if request.method == 'POST':
        iiid=request.POST.get('id')
        iid=iiid[1:]

        menuInst=Products.objects.get(id=int(iid))
        if Cart.objects.filter(user=request.user).filter(ItemID=menuInst).exists():
            x=Cart.objects.filter(user=request.user).get(ItemID=menuInst)
            x.Quantity=x.Quantity+1
            x.save()
        else:
            x=Cart(user=request.user,ItemID=menuInst,Quantity=1)
            x.save()
    return JsonResponse({'res':'ok'})

@login_required(login_url='Login')
def cart(request):
    usr=request.user
    if Address.objects.filter(Name=usr).exists():
        cart=Cart.objects.filter(user=usr)
        totalprice=0
        print(len(cart))
        if len(cart) == 0:
            mt=True
        else:
            mt=False
        for c in cart:
            price=c.ItemID.Price
            total=price*c.Quantity
            totalprice=totalprice+total
        # print(totalprice)
        return render(request,'cart.html',{'cart':cart,'tprice':totalprice,'m':mt})
    else:
        return render(request,'address.html')

@login_required(login_url='Login')
def address(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        if Address.objects.filter(Name=request.user).exists():
            x=Address.objects.get(Name=request.user)
            x.Name=request.user
            x.Phone=phone
            x.address=name+'\n'+address
            x.save()
        else:
            x=Address(Name=request.user,Phone=phone,address=name+'\n'+address)
            x.save()
            return cart(request)
    return render(request,'address.html')
    
@login_required(login_url='Login')
def order(request):
    if request.method == 'POST':
        cart=Cart.objects.filter(user=request.user)
        if len(cart) == 0:
            return render(request,'thanks.html')
        totalprice=0
        items=''
        try:
            for c in cart:
                price=c.ItemID.Price
                total=price*c.Quantity
                totalprice=totalprice+total
                items=items+'\n'+c.ItemID.Item+' X '+str(c.Quantity)+'\n'

                c.delete()

            cust=Address.objects.get(Name=request.user)
            ins=Order(user=request.user,Phone=cust.Phone,Address=cust.address,Items=items,Total=totalprice)
            ins.save()
        except:
            print('pass')
        
    return render(request,'thanks.html')

def products(request):
    pro=Products.objects.all()
    return render(request,'allproducts.html',{'products':pro})

def Login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
  
        else:
            messages.warning(request,'Password or Username does not match!')
            return render(request,'login.html')
        return index(request)
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password1')
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'User Exists!')
            else:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                return Login(request)
        else:
            messages.warning(request,'Password not maching!')
            return render(request,'signup.html')
        
    return render(request,'signup.html')


def search(request,term):
    qs=Products.objects.all()

    for t in term.split():
        qs = qs.filter(Item__icontains = term)
        print(qs)
    return render(request,'allproducts.html',{'products':qs})

def pincode(request):
    return render(request,'location.html')


