from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name= 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('ajax/register/', views.ajax_register, name='ajax_register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url ='/'), name='login'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/',views.profile, name='profile'),
]
