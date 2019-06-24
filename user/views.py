from django.contrib import auth
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
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


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    results = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])
    # 로그인 실패
    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 처리
    # 현재는 객체로 만들어진 상태
    authuser = results[0]
    # 객체를 dictionary 형태로 변경하여 저장
    request.session['authuser'] = model_to_dict(authuser)

    return HttpResponseRedirect('/')
    # user = User.objects.get(email=email, password=password)
    # if user:
    #     # login(request, user=user)
    #     return HttpResponseRedirect('/')
    # else:
    #     return render(request, 'user/loginform.html')


def logout(request):
    # 세션 제거하기
    del request.session['authuser']
    return HttpResponseRedirect('/')


def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    data = {
        'user': user
    }
    return render(request, 'user/updateform.html', data)


def update(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender =  request.POST['gender']
    if request.POST['password'] is not '':
        user.password = request.POST['password']
    else:
        return HttpResponseRedirect('/user/updateform?result=fail')
    user.save()
    request.session['authuser'] = model_to_dict(user)
    return HttpResponseRedirect('/user/updateform?result=success')


# Jquery ajax 통신
def checkemail(request):
    try:
        user = User.objects.get(email=request.GET['email'])
    except Exception as e:
        user = None

    result = {
        'result': 'success',
        'data': 'Not exist' if user is None else 'exist'
    }
    return JsonResponse(result)

