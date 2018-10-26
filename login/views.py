from django.shortcuts import render,redirect,render_to_response
from . import models
from django.http import HttpResponse,HttpResponseRedirect
from .models import Article,Comments,User
from .froms import UserForm,RegisterForm,ArticleForm,CommentsForm
import time,datetime
import hashlib
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
#from django.core.paginator import Paginator

#主页面的返回
def index(request):
    return render(request,'login/index.html')

#用户登录
def login(request):
    # 通过session来判断用户是否已经登录，如果是登录状态，则不可以重复登录
    if request.session.get('is_login',None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


#用户注册
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")#render是渲染变量到模板中,而redirect是HTTP中的1个跳转的函数,一般会生成302状态码
    if request.method == "POST":
        register_form = RegisterForm(request.POST)#获取到用户提交过来的数据
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据是否有效
            username = register_form.cleaned_data['username']#获取用户提交过来的username
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()#保存用户的信息到数据库
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()#实例化RegisterForm
    return render(request, 'login/register.html', locals())

#用户退出
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

#返回给用户全部的博文信息
# def myblog(request):
#    blogs_all_list = Article.objects.all()#获取Article表中的所有数据
#    return render(request,'blog/blog.html',{'blogs_all_list':blogs_all_list})

# class myblog(View):

def myblog(request):
    all_blog = Article.objects.all().order_by('-id')#获取Article表中的全部数据，根据id的降序排列
    # 分页
    try:
        page = request.GET.get('page', 1)#获取页数，默认为1
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blog, 3, request=request)  #5为每页展示的博客数目

    orgs = p.page(page)
    return render(request, 'blog/blog.html', {'all_blog': orgs,})



#自己写博文的方法
def blogwen(request):
    if request.method == 'POST':
        blogwen_form = ArticleForm(request.POST)
        message = "请检查填写的内容！"
        if blogwen_form.is_valid():
            articletitle = blogwen_form.cleaned_data['articletitle']
            articlecontent = blogwen_form.cleaned_data['articlecontent']
            new_blogwen = models.Article.objects.create()
            new_blogwen.title = articletitle
            new_blogwen.content = articlecontent
            new_blogwen.pub_time = datetime.datetime.now()#当用户提交博文请求时,默认给一个当前时间戳到数据库
            new_blogwen.auser_id = request.session['user_id']
            new_blogwen.save()
            return redirect('/blog/')
    blogwen_form = ArticleForm()
    return render(request,'blog/blogwen.html', locals())

#评论
def comments(request,comments_id):
    # if request.session.get('comments_id',None):
    #     return redirect('/blog/')
    if request.method == "POST":
        comments_form = CommentsForm(request.POST)#获取到用户提交过来的数据
        message = "请检查填写的内容！"
        if comments_form.is_valid():  # 获取数据是否有效
            comments_contents = comments_form.cleaned_data['comments_contents']#获取用户提交过来的username

            #保存数据
            # comments = Comments.objects.get(id=comments_id)
            # user_list = comments.user.all()

            new_comments = models.Comments.objects.create()
            # new_comments.id = comments_id
            new_comments.comments_name = request.session['user_name']#获取登录时的用户名
            new_comments.comments_content = comments_contents
            new_comments.comments_time = datetime.datetime.now()#当用户提交博文请求时,默认给一个当前时间戳到数据库
            new_comments.article_c_id = comments_id
            new_comments.save()
            return redirect('/blog/')
    comments_form = CommentsForm()

    return render(request,'blog/comments.html',{'comments_form':comments_form,'comments_id':comments_id})


#对密码进行hash加密的方法,使用户账号更加的安全
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def page(request):
    page = Article.objects.all()
    return render(request,'blog/blog.html',{'page':page})

#用于博文分页
def article(request,article_id):
    article_all = Article.objects.get(id=article_id)
    # comments_all = Comments.objects.get(id=article_id)
    article = get_object_or_404(Article,id=article_id)

    #正向查询
    # comments = Comments.objects.get(id=article_id)
    # user_list = comments.user.all()
    
    article_c = Article.objects.get(id=article_id)
    comments_list = article_c.comments_set.all()
    return render(request,"blog/article.html",locals())

#删除数据
def delete_data(request,delete_id):
    article_u = Article.objects.get(id=delete_id)
    auser = article_u.auser
    if auser.name == request.session['user_name']:

        dels = Article.objects.get(id=delete_id)
        dels.delete()
        return HttpResponseRedirect('/blog/')
    else:
        return HttpResponse('对不起，你没有删除权限')

#我的博文
def my_blog(request):
    #一对多的关联
    auser = User.objects.get(name=request.session['user_name'])
    article_list = auser.article_set.all()

    # article_all = article_list.order_by('-id')
    # # 分页
    # try:
    #     page = request.GET.get('page', 1)#获取页数，默认为1
    # except PageNotAnInteger:
    #     page = 1
    # p = Paginator(article_all, 3, request=request)  #5为每页展示的博客数目

    # orgs = p.page(page)
    return render(request,'blog/myblog.html',{"article_list":article_list})

# def myblog(request):
#     all_blog = Article.objects.all().order_by('-id')#获取Article表中的全部数据，根据id的降序排列
#     # 分页
#     try:
#         page = request.GET.get('page', 1)#获取页数，默认为1
#     except PageNotAnInteger:
#         page = 1
#     p = Paginator(all_blog, 3, request=request)  #5为每页展示的博客数目

#     orgs = p.page(page)
#     return render(request, 'blog/blog.html', {'all_blog': orgs,})

# 个人详情页
def gerenxiangqing(request):
    ren_user = User.objects.get(id=request.session['user_id'])
    ren_user.password = "******"
    register_form = RegisterForm()
    return render(request,'blog/gerenxiangqing.html',locals())

def xiugai(request):
    ren_user = User.objects.get(id=request.session['user_id'])
    ren_user.password = "******"
    register_form = RegisterForm()
    return render(request,'blog/xiugai.html',locals())