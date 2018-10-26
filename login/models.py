from django.db import models
from time import ctime 
from django.urls import reverse

#用户表
class User(models.Model):
    '''用户表'''

    gender = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(verbose_name='用户名',max_length=128,unique=True)#用户名称
    password = models.CharField(verbose_name='密码',max_length=256)#用户密码
    email = models.EmailField(verbose_name='邮箱',unique=True)#用户邮箱
    sex = models.CharField(verbose_name='性别',max_length=32,choices=gender,default='男')#用户性别,默认为男性
    c_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)#创建用户的时间


    #使对象在后台显示更友好
    def __str__(self):
        return self.name

    # 使后台更易于管理(是中文)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']

#文章表
class Article(models.Model):
    title = models.CharField(verbose_name='标题',max_length=100)#文章标题
    content = models.TextField(verbose_name='正文',blank=True,null=True)#文章正文
    pub_time = models.DateTimeField(verbose_name='发布时间',blank=True,null=True)#文章发布时间

    #关联  User  表
    auser = models.ForeignKey(User,verbose_name='用户',null=True,on_delete=models.CASCADE)#和  User  进行关联一对多的操作

    #使对象在后台显示更友好
    def __str__(self):
        return self.title

    class Meta:
        verbose_name='博客'
        verbose_name_plural = verbose_name
        ordering = ["-pub_time"]

        

#评论表
class Comments(models.Model):
    comments_name = models.CharField(verbose_name='评论人',max_length=128,null=True)#用户名称
    comments_content = models.TextField(verbose_name='评论文',blank=True,null=True)#评论正文
    comments_time = models.DateTimeField(verbose_name='评论时间',blank=True,null=True)#评论发布时间  

    #关联  User  表
    user = models.ManyToManyField(User)#和  User  进行关联多对多的操作

    article_c = models.ForeignKey(Article,verbose_name='文章',null=True,on_delete=models.CASCADE)

    #使对象在后台显示更友好
    def __str__(self):
        return self.comments_name      
        
    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name
        ordering = ['-comments_time']

