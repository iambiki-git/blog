from django.contrib import admin
from .models import CustomUser, Post, Notification, Like
# Register your models here.

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'username', 'email', 'user')
#     search_fields = ('username', 'email')

# admin.site.register(CustomUser, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at', 'is_approved')

admin.site.register(Post, PostAdmin)



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')   

admin.site.register(Notification, NotificationAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'liked_at')

admin.site.register(Like, LikeAdmin)