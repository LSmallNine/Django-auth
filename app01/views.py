from django.shortcuts import render,redirect,HttpResponse
#引入 auth 模块
from  django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd= request.POST.get('pwd')
        # 验证用户是否存在
        user = authenticate(username=user,password=pwd)

        if  user :
            auth.login(request,user) #request.user  :当前登录用户
            next_url = request.GET.get("next", "/index/")
            #  这么写的目的如果没有权限的用户访问index就会在url中提示/login/?next=/index/
            return  redirect(next_url)
            # return redirect("/index/")
    return render(request,'login.html')

#用户效验
#方式一
#登录装饰器
@login_required()
def index(request):
    #这里不用传递参数，因为request是全局变量
    return render(request,'index.html')

#方式二
# def my_view(request):
#   if not request.user.is_authenticated():
#     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


#注销
def logout(request):
    auth.logout(request)
    return redirect('/login/')


#注册
def reg(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = User.objects.create_user(username=user,password=pwd)
        return redirect('/login/')
    return render(request,'reg.html')

#修改密码
@login_required()
def edit_pwd(request):

    user = request.user
    state = ''
    if request.method == 'POST':
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        repeat_pwd =request.POST.get('repeat_pwd')
        if user.check_password(old_pwd):
            if not new_pwd:
                state ='error'
            elif new_pwd != repeat_pwd:
                state = 'repeay_error'
            else:
                user.set_password(new_pwd)
                user.save()
                return  redirect('/login/')
        else:
            state = 'passowrd_error'
    content ={
        'user':user,
        'stat':state
    }
    return render(request,'edit_pwd.html',locals())


