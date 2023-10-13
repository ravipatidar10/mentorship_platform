from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from mentor.models import Mentor
from mentee.models import Mentee

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email).first()
    if not user:
        return render(request, 'users/login.html', {"error": "User with this credentials does not exists."})
    user = auth.authenticate(request, username=user.username, password=password)
    if not user:
        return render(request, 'users/login.html', {"error": "User with this credentials does not exists."})
    # print(User.objects.first().__dict__)
    auth.login(request, user)
    return HttpResponse("Login successfull")
    
def signup(request):
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
    return HttpResponse("Success")
