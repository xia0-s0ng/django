from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
     list_display=['name','email','sex','c_time']#定在 列表页 中能够显示的字段们
     list_display_links=['name','email']#允许被连接到详情页的字段们
     search_fields=['name','sex']#允许被搜索的字段
     list_filter=['name','email']#右侧添加过滤器
     date_hierarchy='c_time'#增加时间过滤器
     fieldsets=(
            #分组1
            (
                '基本信息',{
                    'fields':('name','email','sex'),
                }
            ),
        )

class ArticleAdmin(admin.ModelAdmin):
     list_display=['title','content','pub_time']#定在 列表页 中能够显示的字段们
     list_display_links=['title','content']#允许被连接到详情页的字段们
     search_fields=['title','content']#允许被搜索的字段
     list_filter=['title']#右侧添加过滤器
     date_hierarchy='pub_time'#增加时间过滤器

class CommentsAdmin(admin.ModelAdmin):
     list_display=['comments_name','comments_content','comments_time']#定在 列表页 中能够显示的字段们
     list_display_links=['comments_name','comments_content']#允许被连接到详情页的字段们
     search_fields=['comments_name']#允许被搜索的字段
     list_filter=['comments_name']#右侧添加过滤器
     date_hierarchy='comments_time'#增加时间过滤器

admin.site.register(models.User,UserAdmin)#注册User类
admin.site.register(models.Article,ArticleAdmin)#注册Article类
admin.site.register(models.Comments,CommentsAdmin)#注册Comments类