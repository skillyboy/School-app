import uuid
# from winsound import MessageBeep
from attr import field
# from matplotlib.style import available
# from django.db.models.query_utils import subclasses
import requests
import json
from django.http import HttpResponse
from . forms import SignupForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Faculty, Department,Courses, Mycourse, Payment, Wishlist,Forum,Message, Note, Picture
import datetime

# Create your views here.



@login_required(login_url='/login')
def new(request):
    return render(request, 'new.html')

def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            new = reg.save()
            login(request, new)
            messages.success(request, 'Signup successfull!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signupform')

    context = {
        'reg': reg
    }

    return render (request,'signup.html', context)


def logoutfunc(request):
    logout(request)
    return redirect('index')


def loginfunc(request):  
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            # messages.success(request, 'successful')
            return redirect('index')
        else:
            # messages.warning(request, 'username/password incorrect')
            return redirect('login')
    return render (request, 'login.html')


def password(request):
    update = PasswordChangeForm(request.user)
    if request.method == 'POST':
        update = PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Password update successful!')
            return redirect('index')
        else:
            # messages.error(request, update.errors)
            return redirect('password')

    context = {
        'update': update
    }

    return render(request, 'password.html', context)




@login_required(login_url='/login')
def dashboard(request):  

    
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def resume(request):  
    return render(request, 'resume.html')

def bio(request):
    return render(request, 'bio.html')

def profile(request):
    return render(request, 'profile.html')

def index(request):
    skills = Faculty.objects.all()
    category = Department.objects.all()
    courses = Courses.objects.all()

    context={
        'skills': skills,
        'category': category ,
        'courses': courses,       
    }

    return render(request, 'index.html',context)

@login_required(login_url='/login')
def courses(request):  
    courses= Courses.objects.all()

    context={
        'courses': courses,
    }

    return render(request, 'courses.html',context)

@login_required(login_url='/login')

def category(request,id):
    category = Faculty.objects.get(id=id)

    context={
        'category ': category ,
    }

    return render(request, 'category.html',context)

def content(request,id):  
    # content = Content.objects.filter(content_id=id)
    
    content = Note.objects.all()
    # content = Note.objects.get(pk=id)

    # content = Note.objects.get(content_id=id)
    
    
    context={
        'content': content, 
    }
    return render(request, 'content.html', context)

def course(request,id):  
    course = Courses.objects.get(pk=id)

    context={
        'course': course, 
    }
    return render(request, 'course.html', context)


def categorys(request):  
    categorys = Department.objects.all()

    context={
        'categorys': categorys, 
    }
    return render(request, 'categorys.html', context)

def tech(request,id):  
    tech = Courses.objects.filter(depart_id=id)

    context={
        'tech': tech, 
    }
    return render(request, 'tech.html', context)


@login_required(login_url='/login')
def wishlist(request):
    wishlist = Courses.objects.filter(pk = request.user.pk, paid=False)

    return render(request, 'wishlist.html')


def skills (request):
    return render(request, 'skills.html')


def music (request):
    return render(request, 'music.html')


def socials (request):
    return render(request, 'socials.html')
        


def uploaddp (request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def addtowish(request):
    if request.method == 'POST':
        refrence = str(uuid.uuid4())
        identity= request.POST['skill']
        item = Courses.objects.get(pk=identity)
        userlikes = Wishlist.objects.filter(user__username= request.user.username )
        if userlikes:
            order = Wishlist.objects.filter(user__username=request.user.username,thecontent_id= item.id).first()
            if order:
                
                if order.paid == False :
                    order.save()
                    # messages.success(request, 'Skill has been added to you wishlist')
                else:
                    # messages.success(request, 'Course content already purchased !') 
                    return redirect('mycourses')                    

            else:
                    # this runs when a new item is added to the basket 
                newbasket = Wishlist()
                newbasket.user = request.user
                newbasket.thecontent= item
                newbasket.paid = False
                # newbasket.available=False

                newbasket.save() 
                # messages.success(request, 'Skill has been added to you wishlist !') 
        else:
            # this is when a basket is to be created for the first time 
            basket = Wishlist()
            basket.user = request.user
            basket.thecontent = item
            basket.paid = False
            # basket.available=False
            basket.save() 
            # messages.success(request, 'Skill has been added to you wishlist!')
    return redirect('wishlist')

def wishlist(request):
    wishlist = Wishlist.objects.filter(user__username=request.user.username, paid=False)
    
    subtotal=0
    discount=0
    total=0

    for item in wishlist:
        subtotal += item.thecontent.fee

    discount=0.00* subtotal

    total=subtotal - discount

    context={
        'wishlist': wishlist, 
        'subtotal':subtotal,
        'discount':discount,
        'total':total
    }
    return render(request, 'wishlist.html',context)

def deleteitem(request):
    itemid=request.POST['skill']
    Wishlist.objects.filter(pk=itemid).delete()
    # messages.success(request, 'Product deleted')
    return redirect ('wishlist')


def checkout(request):
    wishlist = Wishlist.objects.filter(user__username = request.user.username,paid=False)
    
    subtotal=0
    discount=0
    total=0

    for item in wishlist:
        subtotal += item.thecontent.fee

    discount=0.10* subtotal

    total=subtotal - discount  
    
    context = {
        'wishlist': wishlist,
        'subtotal':subtotal,
        'discount':discount,
        'total':total
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='/login')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_4b0e1d9d7d91ebed3107222a4dd563a987d740b3'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://54.210.222.113/completed'
        # cburl= 'http://localhost:8000/completed/'
        total = float(request.POST['total']) * 100
        pay_code = str(uuid.uuid4())
        user = User.objects.get(username=request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        
        # collect data that you will send to paystack
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': pay_code, 'email': user.email,'amount':int(total), 'callback_url': cburl}

        # make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.warning(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            paid = Payment()
            paid.user = user
            paid.fee = total
            paid.paid = True
            paid.pay_code = pay_code
            paid.first_name = first_name  
            paid.last_name = last_name
            paid.phone = phone
            paid.save()

            reserve = Wishlist.objects.filter(user__username=request.user, paid=False)
            for item in reserve:
                item.paid = True
                item.fee = total
                item.save()

                book =Courses.objects.get(pk=item.thecontent.id)
                book.save()
            
            return redirect(rd_url)
    return redirect('completed')


def completed(request):
    client = User.objects.get(username=request.user.username)
    paid = Wishlist.objects.filter(user__username=request.user.username, paid=True)

    context={
        'client':client,
        'paid':paid,
       
    }
    return render(request, 'completed.html', context)


@login_required(login_url='/login')
def mycourses(request):  
    client = User.objects.get(username=request.user.username)
    paid = Wishlist.objects.filter(user__username=request.user.username, paid=True)

    context={
        'client':client,
        'paid':paid,     
    }
    return render(request, 'mycourses.html', context)





def newgroup(request):
    return render(request, 'newgroup.html')

def creator(request):
    room= request.POST['room_id']

    if Forum.objects.filter(name=room).exists():
        return HttpResponse("This group already exists")
    else: 
        newgroup = Forum.objects.create(name=room)  
        newgroup.save()
        return redirect('groups')

def groups(request):
    groups= Forum.objects.all()
 
    context={
        'groups': groups,
    }
    return render(request, 'groups.html', context)

def forum(request,id):
    forum = Forum.objects.get(pk=id)

    context={
        'forum':forum,  
    }  
    return render(request, 'forum.html', context)


def messenger(request,id):
    forum = Forum.objects.get(pk=id)
    chatboard = Message.objects.filter(forum_id=id)

    context={
        'forum': forum,
        'chatboard':chatboard,    
    }  
    return render(request, 'messenger.html', context)


def send(request):
    user = User.objects.get(username = request.user.username)
    room = request.POST['forum.id']
    spec = Forum.objects.get(id=room)
    message= request.POST['message']
    new_message = Message()
    # new_message.forum = Message.objects.create(value=message, forum_id =spec)    
    if request.method == 'POST':
        new_message.sender = user
        new_message.forum = spec
        new_message.value = message
        new_message.save()
        return redirect('messenger')

# def send(request):
#     spec = Forum.objects.get(pk=id)
#     message= request.POST['message']
#     new_message= Message.objects.create(value=message, forum_id= spec.id)
#     new_message.save()
#     return render(request,'messenger.html')


# def send(request):
#     room = request.POST['forum.id']
#     spec = Forum.objects.get(id=room)
#     message= request.POST['message']
#     if request.method == 'POST':
#         new_message= Message.objects.create(value=message, forum_id =spec)
#         new_message.save()
#     return redirect('messenger')

def search(request):  
    if request.method == 'POST':
        searched = request.POST['search']
        # if Room.objects.filter(name=room).exists():
        course = Courses.objects.filter(coding__contains=searched)
        return render(request, 'courses.html', {'searched': searched, 'course': course})
    else: 
        return render(request, 'courses.html', {})

def search(request):
    searched= request.POST['input']

    if Courses.objects.filter(name=searched).exists():
        forum = Courses.objects.get(pk=id)
    else: 
        return HttpResponse("This group already exists")
        
        # newgroup = Forum.objects.create(name=room)  
        # newgroup.save()
        # return redirect('groups')

# def pick (request):
#     user = authenticate(request, username= request.user.username, password=password)
#     if request.method == 'POST':
#         pck= request.POST['item7']
#         choice = Wishlist.objects.get(pk=pck)
#         field = Wishlist.objects.filter(category_id=choice.id)
#         if field:
#             category=Category.objects.all() 
#             return redirect('course') 
#         else:
#             # messages.info(request, 'The room is not available for the dates you specified, kindly choose another date. Thank you')
#             return render(request, 'course.html')
#     return render(request, 'course.html')