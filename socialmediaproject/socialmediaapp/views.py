from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post,Like,FollowerCount
from django.contrib.auth.decorators import login_required
from django.db.models.fields.files import ImageFieldFile
from itertools import chain


# Create your views here.
@login_required(login_url='loginuser')
def index(request):
    user_obj=User.objects.get(username=request.user.username)
    profile_obj=Profile.objects.get(user=user_obj)
    post_obj=Post.objects.all()

    user_following_list=[]
    feed_lists=[]

    user_following=FollowerCount.objects.filter(follower=request.user.username)
    
    for following in user_following:
        user_following_list.append(following.user)

    for users in user_following_list:
        feed=Post.objects.filter(user=users)
        feed_lists.append(feed)

    feeds=list(chain(*feed_lists))

    
    return render (request,'index.html',{'profile_obj':profile_obj, 'feeds':feeds})


def likepost(request):
    username=request.user.username
    id=request.GET.get('post_id')
    post=Post.objects.get(id=id)
    like_user=Like.objects.filter(post_id=id,username=username).first()
    
    if like_user is None:
        like_post=Like.objects.create(post_id=id,username=username)
        like_post.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')

    else:
        like_user.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')



# here follower is current user and user is who is  followed by follower
    
def follower(request):
    if request.method == 'POST':
        user=request.POST['user']
        follower=request.POST['followers']

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delfollower =FollowerCount.objects.get(follower=follower, user=user)
            delfollower.delete()
            return redirect ('index')
        else:
            new_follower=FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
   
            return redirect ('profileuser/'+ user)
        
    
        



def profileuser(request,pk):
    user_obj=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_obj)
    user_posts=Post.objects.filter(user=pk)
    length_post=len(user_posts)

    user=pk
    follower= request.user.username
    
    if FollowerCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'

    else:
        button_text = 'Follow'

    followers=len(FollowerCount.objects.filter(user=pk))
    following=len(FollowerCount.objects.filter(follower=pk))


    data={
         'user_obj':user_obj,
         'user_profile':user_profile,
         'user_posts':user_posts,
         'length_post':length_post,
         'followers':followers,
         'following': following,
         'button_text': button_text,
    }

    return render(request,'profile.html',data)
    

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

def uploadpost(request):
    if request.method=="POST":
      user=request.user.username
      image=request.FILES.get('image_upload')
      caption=request.POST['caption']
      new_post=Post.objects.create(user=user,image=image,caption=caption)
      new_post.save()
      return redirect ('/')
    else:
        return redirect('/')


def settinguser(request):
    profileuser=Profile.objects.get(user=request.user)
    if request.method=="POST":
      if request.FILES.get('profile_pic') is None:
          profile_pic=profileuser.profile_pic
          bio=request.POST['bio']
          location=request.POST['location']
          print(bio,location)
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
    