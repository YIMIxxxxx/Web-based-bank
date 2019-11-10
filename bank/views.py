from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms


def index(request):
    # 客户主页（查余额/转账）
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('is_staff', None):   #权限隔离
        request.session.flush()
        return redirect('/login/')

    user = models.AccntInfo.objects.get(user_name=request.session.get('user_name', None))

    if request.method == "POST":
        trans_form = forms.TransForm(request.POST)
        if trans_form.is_valid():
            dest_accnt = trans_form.cleaned_data.get('dest_accnt')
            amnt = trans_form.cleaned_data.get('amnt')

            try:
                # 查询数据库中的目的账户是否存在
                dest_user = models.AccntInfo.objects.get(accnt_num=dest_accnt)
            except:
                message = '目的账户不存在！'
                return render(request, 'login/index.html', locals())
            if dest_user.is_valid == 0:  #已销户
                message = '目的账户不存在！'
                return render(request, 'login/index.html', locals())

            if amnt > user.bal: # 转账金额超过当前用户余额
                message = '余额不足！'
                return render(request, 'login/index.html', locals())

            # 转账成功，修改数据库
            user.bal -= amnt
            dest_user.bal += amnt
            trans_info = models.TransInfo(
                source_accnt=user.accnt_num, dest_accnt=dest_accnt, amnt=amnt)
            trans_info.save()
            user.save()
            dest_user.save()
            message = '转账成功！'
            trans_form = forms.TransForm()
            return render(request, 'login/index.html', locals())
    trans_form = forms.TransForm()
    return render(request, 'login/index.html', locals())


def login(request):
    # 客户登录
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

            if user.is_valid == 0:  #已销户
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.user_passwd == password:    # 验证密码
                request.session['is_login'] = True
                request.session['is_staff'] = False
                request.session['user_passwd'] = user.user_passwd
                request.session['user_name'] = user.user_name
                request.session['accnt_num'] = user.accnt_num
                request.session['bal'] = user.bal
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
    # 职员登录
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/manage/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                staff = models.StaffInfo.objects.get(staff_id=username)  # 查询数据库中的职员id
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
            message = '请填写用户名和密码！'
            return render(request, 'login/staff_login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/staff_login.html', locals())


def manage(request):
    # （职员）管理页面（开户/销户）
    if not request.session.get('is_login', None):
        return redirect('/staff_login/')
    if not request.session.get('is_staff', None):   #权限隔离
        request.session.flush()
        return redirect('/staff_login/')

    if request.method == "POST":
        add_form = forms.UserForm(request.POST)
        del_form = forms.DelForm(request.POST)
        if add_form.is_valid():     # 开户
            user_name = add_form.cleaned_data.get('username')
            user_passwd = add_form.cleaned_data.get('password')
            user = models.AccntInfo(
                user_name=user_name, user_passwd=user_passwd, bal=0, is_valid=1)
            user.save()
            message = '添加成功！accnt_num=' + str(user.accnt_num)
            add_form = forms.UserForm()
            del_form = forms.DelForm()
            return render(request, 'login/manage.html', locals())

        if del_form.is_valid():     # 销户
            del_accnt = del_form.cleaned_data.get('del_accnt')
            del_passwd = del_form.cleaned_data.get('password')

            try:
                # 查询数据库中的销户账户是否存在
                del_user = models.AccntInfo.objects.get(accnt_num=del_accnt)
            except:
                message2 = '账户不存在！'
                return render(request, 'login/manage.html', locals())
            if del_user.is_valid == 0:  #已销户
                message2 = '账户不存在！'
                return render(request, 'login/manage.html', locals())
            if not del_user.user_passwd == del_passwd:
                message2 = '密码错误！'
                return render(request, 'login/manage.html', locals())
            # 修改数据库
            del_user.is_valid = 0
            del_user.save()
            message2 = '销户成功！'
            del_form = forms.DelForm()
            add_form = forms.UserForm()
            return render(request, 'login/manage.html', locals())

    add_form = forms.UserForm()
    del_form = forms.DelForm()
    return render(request, 'login/manage.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 没登录不能登出
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def toindex(request):
    return redirect("/index")