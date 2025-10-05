from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # home or other app urls...
    path('', views.home, name='home'),

    # Registration
    path('register/', views.register, name='register'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Login and Logout using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
