from django.contrib import admin
from .models import Profile, About,Post, Like, Comment,Message, Notification,Mention

admin.site.register(Profile)
admin.site.register(About)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Mention)
