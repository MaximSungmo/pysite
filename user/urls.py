"""python_ch3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

import user.views as user_views


urlpatterns = [

    # 회원가입
    path('joinform/', user_views.joinform),
    path('join', user_views.join),
    path('joinsuccess', user_views.joinsuccess),

    # 로그인
    path('loginform', user_views.loginform),
    path('login', user_views.login),

    # 로그아웃
    path('logout', user_views.logout),

    # 업데이트
    path('updateform', user_views.updateform),
    path('update', user_views.update),

    # 이메일 중복체크
    path('api/checkemail', user_views.checkemail),

]
