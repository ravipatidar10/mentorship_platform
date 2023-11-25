# 3rd Party Import
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Local Import
from mentor.models import Mentor
from mentee.models import Mentee

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if Mentor.objects.filter(user=request.user).exists():
                role = "mentor"
                return redirect('mentor_dashboard')
            else:
                role = "mentee"
                return redirect('mentee_dashboard')
        else:
            return render(request, 'users/login.html')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email).first()
    if not user:
        return render(request, 'users/login.html', {"error": "User with this credentials does not exists."})
    # user = auth.authenticate(request, username=user.username, password=password)
    
    if not user:
        return render(request, 'users/login.html', {"error": "User with this credentials does not exists."})
    # print(User.objects.first().__dict__)
    auth.login(request, user)
    return redirect("login")
    
def signup(request):
    """
    User Registration
    Method type:GET/POST
    Parameters:
        email
        password
        username
        mentee
        mentor
    """
    if request.method == 'GET':
        return render(request, 'users/signup.html')
    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('username')
    mentee = request.POST.get('mentee')
    mentor = request.POST.get('mentor')

    if mentor and mentee:
        return render(request, 'users/signup.html', {"error": "Something went wrong"})
    
    if User.objects.filter(email=email).exists():
        return render(request, 'users/signup.html', {"error": "Email already exists."})
    if User.objects.filter(username=username).exists():
        return render(request, 'users/signup.html', {"error": "Username already exists."})
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    auth.login(request, user)
    if mentee:
        Mentee(user=user).save()
    elif mentor:
        Mentor(user=user).save()
    return redirect('login')

@login_required(login_url='/')
def signout(request):
    """
    Handle User logout 
    Method type:GET 
    """
    auth.logout(request)
    return redirect('login')

@login_required(login_url='/')
def update(request):
    """
      updating the first name and last name of a user and redirecting them to either the mentor or mentee dashboard based on their role
      Method type:POST
      Parameters:
           first_name
           last_name
            role
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    role = request.POST.get('role')
    user = request.user
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    if role == 'mentor':
        return redirect('mentor_dashboard')
    else:
        return redirect('mentee_dashboard')
    

