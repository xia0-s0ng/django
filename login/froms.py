from django import forms
import time
from datetime import datetime

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)

class ArticleForm(forms.Form):
    articletitle = forms.CharField(label='文章标题',max_length=100)
    articlecontent = forms.CharField(label='文章正文',widget=forms.Textarea)
    # articlectime = forms.DateTimeField(label='创建时间',widget=forms.DateTimeInput)

class CommentsForm(forms.Form):
    # comments_names = forms.CharField(max_length=128)#用户名称
    comments_contents = forms.CharField(label='正文',widget=forms.Textarea)#评论正文
    # comments_times = forms.DateTimeField(verbose_name='发布时间',blank=True,null=True)#评论发布时间

