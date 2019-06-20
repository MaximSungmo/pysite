from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    user = User()
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()
    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def login(request):
    if request.method == "GET":
        return render(request, 'user/loginform.html')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email, password=password)
        if user:
            # login(request, user=user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'user/loginform.html')


