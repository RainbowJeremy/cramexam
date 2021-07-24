from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.ArticleListView.as_view() , name='blog-list'),
    path('detail/<pk>/', views.ArticleDetailView.as_view() , name='detail'),
    path('create/', views.ArticleCreateView.as_view() , name='create-blog'),
    path('update/<pk>/', views.ArticleUpdateView.as_view() , name='update-blog'),

    
]