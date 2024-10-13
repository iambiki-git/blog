from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import CustomUser, Post, Notification
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.filter(is_approved=True).order_by('-created_at')[:6]
    if request.user.is_authenticated:
        new_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        new_notifications_count = 0

    content = {
        'all_posts':posts,
        'new_notifications_count':new_notifications_count,
    }
    return render(request, 'blog/index.html', content)

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, "Login Successful! ")
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password..') 

    return render(request, 'blog/login.html')

def register(request):
    error_messages = []

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if password != confirmPassword:
            error_messages.append("Passwords do not match!")
        #check if username or email already exists
        if User.objects.filter(username=username).exists():
            error_messages.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            error_messages.append("Email already exists.")
        
        if not error_messages:
            user = User.objects.create(
                username = username,
                email = email, 
                first_name = firstname,
                last_name = lastname 
            )
            #hash and set the password securly
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration Successful! Please login.')
            return redirect('signin')

    return render(request, 'blog/register.html', {'error':error_messages})

def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('signin')

@login_required
def profile(request):
    if request.user.is_superuser:
        post = Post.objects.all().order_by('-created_at')
    else:
        post = Post.objects.filter(user=request.user).order_by('-created_at')
    
    if request.user.is_authenticated:
        new_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        new_notifications_count = 0
    
    paginator = Paginator(post, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    content = {
        'page_obj':page_obj,
        'new_notifications_count':new_notifications_count,
    }
    return render(request, 'blog/profile.html', content)

@login_required
def createPost(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

    new_post = Post.objects.create(
        user=request.user,
        title=title,
        content=content
    )
    new_post.save()
    return redirect('profile')

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        # messages.success(request, 'Post updated successfully.')
        return redirect('profile')
    
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_superuser or post.user == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully.')

        #create notification if deleted by admin
        if request.user.is_superuser:
            Notification.objects.create(
                user = post.user,
                message = f"Your post '{post.title}' created on {post.created_at.strftime('%Y-%m-%d')} was deleted by admin."
            )     
    else:
        messages.error(request, 'You do not have permission to delete this post.')

    return redirect('profile')


def readMore(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = {
        'post':post,
    }
    return render(request, 'blog/readMore.html', content)

from .models import Contactus
def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        user_message = Contactus.objects.create(
            user = request.user,
            name = name,
            email = email, 
            message = message
        )
        user_message.save()
        messages.success(request, 'Thank you for contacting us! We have received your message and will get back to you shortly.')
        return redirect('index')

def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.is_approved = not post.is_approved
        post.save()
        return redirect('profile')
    
def notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications.update(is_read=True)
    

    context = {
        'notifications':notifications,
    }
    return render(request, 'blog/notification.html', context)