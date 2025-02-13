from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from .models import Rooom,Topic,Messages,User

from .forms import RooomForm,UserForm,MyUserCreationForm



# Create your views here.

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method=='POST' :
        email=request.POST.get('email').lower()
        
        password=request.POST.get('password')
       # print(email,password)
        try:
            user=User.objects.get(email=email)
            print(user.password)

        except:
            messages.error(request,'User Not Exist ')
        
        user=authenticate(request,email=email,password=password)

        print(user)
        if user:
            print("done")
        if user is not None:
            print("done")
            login(request,user)
            return redirect('home')

        else:
            messages.error(request,'Username and password not exist')
 
 
    context={'page':page}
    return render (request,'temp/login_register.html',context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def RegisterUser(request):
    form=MyUserCreationForm ()


    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
        #   messages.error(request,'An Error Occured During Registration ! ')
    context={'form':form}
    return render (request,'temp/login_register.html',context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms=Rooom.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )


    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q))[0:3]
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'temp/home.html',context)


def room(request,pk):
    room=Rooom.objects.get(id=pk)
    room_messages=room.messages_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method =='POST':
        message=Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room',pk=room.id)
    context={'room':room , 'room_messages':room_messages,'participants':participants}
    return render(request,'temp/room.html',context)



def user_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.rooom_set.all()
    room_messages=user.messages_set.all()
    topics=Topic.objects.all()

    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'temp/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form =RooomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
       
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Rooom.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request, 'temp/room_form.html',context )

@login_required(login_url='login')
def update_room(request,pk):
    room=Rooom.objects.get(id=pk)
    form=RooomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host  :
        return HttpResponse('You are not Allowed ')

    context={'form':form,'topics':topics,'room':room}
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'temp/room_form.html',context)

@login_required(login_url='login')

def delete_room(request,pk):

    room=Rooom.objects.get(id=pk)

    if request.user != room.host  :
        return HttpResponse('You are not Allowed ')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'temp/delete.html',{'obj':room})




@login_required(login_url='login')

def delete_message(request,pk):

    message=Messages.objects.get(id=pk)

    if request.user != message.user  :
        return HttpResponse('You are not Allowed ')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'temp/delete.html',{'obj':message})



@login_required(login_url='login')
def updateuser(request):
    user=request.user
    form= UserForm(instance=user)
    if request.method =='POST':
         form= UserForm(request.POST,request.FILES, instance=user)
         if form.is_valid:
             form.save()
             return redirect('user_profile',pk=user.id)

    return render(request,'temp/update-user.html',{'form':form})



def topicspage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'temp/topics.html',{'topics':topics})


def activitypage(request):
    room_messages=Messages.objects.all()
    return render(request,'temp/activity.html',{'room_messages':room_messages})
