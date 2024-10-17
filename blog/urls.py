from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('register/', views.register, name="register"),
    path('signout/', views.signout, name="signout"),
    path('profile/', views.profile, name="profile"),
    path('post/create/', views.createPost, name="createPost"),
    path('posts/edit/<int:post_id>/', views.edit_post, name="editPost"),
    path('posts/delete/<int:post_id>/', views.delete_post, name="delete_post"),
    path('readmore/<int:post_id>/', views.readMore, name="readmore"),
    path('contactus/', views.contactus, name="contactus"),
    path('approve_post/<int:post_id>/', views.approve_post, name="approve_post"),
    path('notification/', views.notification, name="notification"),
    path('updateProfile/', views.updateProfile, name="updateProfile"),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
