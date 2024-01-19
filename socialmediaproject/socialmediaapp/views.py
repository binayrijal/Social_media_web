from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='loginuser')
def index(request):
    return render (request,'index.html')


def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exist')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_obj=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_obj,id_user=user_obj.id)
                new_profile.save()
                messages.success(request,'user create successfully')
                return redirect('signup')

        else:
            messages.info(request,'Password doesnot match')
            return redirect('signup')
    else:
       return render(request,'signup.html')
    

def loginuser(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('loginuser')
    return render(request,'signin.html')


@login_required(login_url='loginuser')
def logoutuser(request):
    auth.logout(request)
    return redirect('loginuser')
    