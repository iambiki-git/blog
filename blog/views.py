from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import CustomUser, Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

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

def profile(request):
    post = Post.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(post, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {
        'page_obj':page_obj,
    }
    return render(request, 'blog/profile.html', content)

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