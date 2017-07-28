from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import User

def showErrors(request,errors):
    for error in errors:
        messages.error(request,error)

def index(request):
    return render(request,'friends_app/index.html')

def homePage(request):
    current_user=User.objects.currentUser(request)
    friends=current_user.friends.all()
    other_users=User.objects.exclude(id__in=friends).exclude(id=current_user.id)

    context={
        'current_user': current_user,
        'users':other_users,
        'friends':friends,
    }

    return render(request,'friends_app/homePage.html', context)

def register(request):
    if request.method=='POST':
        errors=User.objects.validateUser(request.POST)
        if not errors:
            print 'Create User'
            user=User.objects.createUser(request.POST)

            request.session['user_id']=user.id

            return redirect('/homePage')

        showErrors(request,errors)
    return redirect('/')

def login(request):
    if request.method=='POST':
        errors=User.objects.validateLogin(request.POST)
        if not errors:
            user=User.objects.filter(email=request.POST['email']).first()

            if user:
                password=str(request.POST['password'])
                user_password=str(user.password)

                hashed_pw=bcrypt.hashpw(password,user_password)

                if hashed_pw==user_password:
                    request.session['user_id']=user.id

                    return redirect('/homePage')

            errors.append('Invalid account Information')
        showErrors(request,errors)

    return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
    return redirect('/')

def addFriend(request,id):
    if request.method=='POST':
        if 'user_id' in request.session:
            current_user=User.objects.currentUser(request)
            friend=User.objects.get(id=id)

            current_user.friends.add(friend)

            return redirect('/homePage')

    return redirect('/')

def removeFriend(request,id):
    if request.method=='POST':
        if 'user_id' in request.session:
            current_user=User.objects.currentUser(request)
            friend=User.objects.get(id=id)

            current_user.friends.remove(friend)

            return redirect('/homePage')

    return redirect('/')

def profilePage(request,id):
    user=User.objects.get(id=id)
    context={
        'users':user,
    }

    return render(request,'friends_app/profilePage.html',context)
