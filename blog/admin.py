from django.contrib import admin
from .models import CustomUser, Post
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'user')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')

admin.site.register(Post, PostAdmin)