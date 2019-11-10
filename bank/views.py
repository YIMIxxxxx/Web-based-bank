from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

# Create your views here.


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.AccntInfo.objects.get(user_name=username) # 查询数据库中的用户名
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.is_valid == 0:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.user_passwd == password:    # 验证密码
                request.session['is_login'] = True
                request.session['is_staff'] = False
                request.session['user_passwd'] = user.user_passwd
                request.session['user_name'] = user.user_name
                return redirect('/index/')

            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            message = '请填写用户名和密码'
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def staff_login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/manage/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                staff = models.StaffInfo.objects.get(staff_id=username)  # 查询数据库中的用户名
            except:
                message = '用户不存在！'
                return render(request, 'login/staff_login.html', locals())

            if staff.staff_passwd == password:  # 验证密码
                request.session['is_login'] = True
                request.session['is_staff'] = True
                request.session['user_passwd'] = staff.staff_passwd
                request.session['user_name'] = staff.staff_id
                return redirect('/manage/')

            else:
                message = '密码不正确！'
                return render(request, 'login/staff_login.html', locals())
        else:
            message = '请填写用户名和密码'
            return render(request, 'login/staff_login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/staff_login.html', locals())


def manage(request):
    if not request.session.get('is_login', None):
        return redirect('/staff_login/')
    if not request.session.get('is_staff', None):
        return redirect('/staff_login/')
    return render(request, 'login/manage.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


