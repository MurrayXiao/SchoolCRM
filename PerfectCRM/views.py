from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def acc_login(request):
    """登录验证"""
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # print('pass authenticate', user, type(user), username, password)
            login(request, user)
            return redirect(request.POST.get('next','/crm/'))
        else:
            errors_message = 'Wrong username or password!'
            return render(request, 'login.html', {'errors_message':errors_message})


def acc_logout(request):
    """退出登录"""
    logout(request)
    return redirect('login.html')