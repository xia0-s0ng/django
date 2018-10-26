from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
     url(r'^$',views.index),#主页(输入127.0.0.1:8000时所返回的主页面)
     url(r'^index/',views.index),#主页(当用户退出登录时，退出到的主页面)
     url(r'^login/',views.login),#登录页
     url(r'^register/',views.register),#注册页
     url(r'^logout/',views.logout),#退出登录
     url(r'^blog/',views.myblog,name="myblog"),#博文列表
     url(r'^blogwen/',views.blogwen),#发布博文
     url(r'^comments/(?P<comments_id>[0-9]+)/$',views.comments,name='comments_bowen'),#评论博文
     url(r'^article/(?P<article_id>[0-9]+)/$',views.article,name='article'),#用于分页的操作
     url(r'^delete/(?P<delete_id>[0-9]+)/$',views.delete_data,name='delete_data'),#删除某个博文的操作
     url(r'^myblog/',views.my_blog,name='my_blog'),#我的博文
     url(r'^gerenxiangqing/',views.gerenxiangqing),#个人详情页
     url(r'^xiugai/',views.xiugai),# 修改个人信息
]