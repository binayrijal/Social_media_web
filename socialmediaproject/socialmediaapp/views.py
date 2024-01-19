from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
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
                messages.success(request,'user create successfully')
                return redirect('signup')

        else:
            messages.info(request,'Password doesnot match')
            return redirect('signup')
    else:
       return render(request,'signup.html')