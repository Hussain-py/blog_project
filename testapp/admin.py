from django.contrib import admin
from testapp.models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status',]

    #To generate slug field value automatically
    prepopulated_fields={'slug':('title',)}

    #To want filter property take filter list(based on status)
    list_filter=('status','author','created','publish',)

    #for searc field
    search_fields=('title','body')

    #ordering of blog_posts
    ordering=['status','publish']

    #Date wise blog
    date_hierarchy='publish'

    #Date Wise blog
    raw_id_fields=('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']

    list_filter=['post','active','created','updated']

    search_fields=['name','email','body']


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
