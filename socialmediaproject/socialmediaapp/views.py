from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models.fields.files import ImageFieldFile

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
                
                #login the user and redirect to settings page
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                #create profile
                user_obj=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_obj,id_user=user_obj.id)
                new_profile.save()
                
                return redirect('settinguser')

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

def settinguser(request):
    profileuser=Profile.objects.get(user=request.user)
    if request.method=="POST":
      if request.FILES.get('profile_pic') == None:
          profile_pic=profileuser.profile_pic
          bio=request.POST['bio']
          location=request.POST['location']
          profileuser.profile_pic=profile_pic
          profileuser.bio=bio
          profileuser.address=location
          profileuser.save()
      if request.FILES.get('profile_pic') is not None:
          profile_pic=request.FILES.get('profile_pic')
          bio=request.POST['bio']
          address=request.POST['location']

          profileuser.profile_pic=profile_pic
          profileuser.bio=bio
          profileuser.address=address
          profileuser.save()
      else:
          return redirect('settinguser')
          
          
    return render(request,'setting.html',{'profileuser':profileuser})









@login_required(login_url='loginuser')
def logoutuser(request):
    auth.logout(request)
    return redirect('loginuser')
    