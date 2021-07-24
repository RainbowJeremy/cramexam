from django.urls import path
from . import views

app_name = 'mcqgenerator'

urlpatterns = [
    path('', views.file_drop , name='file_drop'),
    path('questions/<pk>/', views.questions , name='questions'),
    path('post/ajax/questions/', views.postQuestion , name='post_question'),
    path('post/ajax/lecture/', views.post_lecture , name='post_lecture'),
    path('questionbank/', views.question_bank , name='question_bank'),
    
]