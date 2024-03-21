from django.shortcuts import render,redirect
from petapp.models import Pet,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail
# Create your views here.
def home(request):
    context={}
    data=Pet.objects.all()
    context['pets']=data
    return render(request,'index.html',context)


def petdetails(request,pid):
    context={}
    data=Pet.objects.filter(id=pid)
    context['pet']=data[0]

    return render(request,'details.html',context)

def userlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        context = {}
        n = request.POST['username']
        p = request.POST['password']
        if n=='' or p=='':
            context['error'] = 'Please enter all the fields'
            return render(request,'login.html',context)
        else:
            user = authenticate(username = n, password= p)
            if user is not None:
                login(request,user)
                context['success'] = 'Logged in successfully'
                return redirect('/')
            else:
                context['error'] = 'Please provide correct details'
                return render(request,'login.html',context)

def userregister(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}
        e=request.POST['email']
        n=request.POST['login']
        p=request.POST['password']
        if e=='' or n=='' or p=='':
            context['error'] ="plase enter all fields"
            return render(request,'register.html',context)
        else:
            context['success'] = " registered sucessfully please login"
            user = User.objects.create(email=e,username=n)
            user.set_password(p)
            user.save()
            return render(request,'login.html',context)

def userlogout(request):
    logout(request)
    return render(request,'index.html')


def addtocart(request,petid):
    userid=request.user.id
    if userid is None:
        context= {}
        context['error']= "login kar na bhai"
        return render (request,'login.html',context)
    else:
        userid =request.user.id
        users=User.objects.filter(id=userid)
        pets=Pet.objects.filter(id=petid)
        cart =Cart.objects.create(pid=pets[0], uid=users[0])
        cart.save()
        messages.success(request,"janvar pinjaree me aa gaya hai")
        return redirect('/')
    
def showmycart(request):
    context ={}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    context['mycart'] = data
    count =len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'mycart.html',context)

def delete(request,cartid):
    data=Cart.objects.filter(id=cartid)
    data.delete()
    return redirect('/')


def confirmorder(request):
    context ={}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    context['mycart'] = data
    count =len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'confirmorder.html',context)

def serachbytype(request,val,):
    # c1 = Q(type="dog")
    # c2 = Q(price=101)
    # data=Pet.objects.filter(c1 & c2)
    data=Pet.objects.filter(type = val) 
    context={}
    context['pets']=data
    return render(request,'index.html',context)

def sortpetbyprice(request,dir):
    col=''
    context={}
    if dir == 'asc':
        col='price'
    else:
        col='price'
    data=Pet.objects.all().order_by(col)
    context['pets']= data
    return render(request,'index.html',context)


def pricerange(request):
    context={}
    min = request.GET['min']
    max = request.GET['max']
    c1 = Q(price__gte = min)
    c2 = Q(price__lte = max)
    data=Pet.objects.filter(c1 & c2)
    context['pets']= data
    return render(request,'index.html',context)

def makepayment(request):
    context={}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    context['mycart'] = data
    count =len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    client = razorpay.Client(auth=("rzp_test_HkubfwbV338ozD","2Hg3ShRVrg2wfYvO2UGPlNhq"))
    data = {"amount":total*100, "currency":"INR","receipt": ""}
    payment = client.order.create(data=data)
    print(payment)
    context['data'] = payment
    return render (request,'pay.html',context)

def placeorder(request):

    return redirect('/order')

def order(request):
        userid = request.user.id
        print("within in place order",userid)
        user = User.objects.filter(id=userid)
        mycart = Cart.objects.filter(uid=userid)
        ordid=random.randrange(1000,9999)
        for cart in  mycart:
            pet = Pet.objects.filter(id = cart.pid.id)
            ord = Order.objects.create(uid =user[0],pid=pet[0],quantity=cart.quantity ,orderid=ordid)
            ord.save()
        mycart.delete()

        msg_body ='order id is '+str(ordid)
        custEmail = request.user.email
        print("userdetails",userid,custEmail)
        send_mail(
            "order placed succesfully",
            msg_body,
            "mpsgroceryapp@gmail.com",
            [custEmail],
            fail_silently=False,
        )

        messages.success(request,"order  placed suceesfully")
        return redirect('/')


def demofn():
    return "welcome"