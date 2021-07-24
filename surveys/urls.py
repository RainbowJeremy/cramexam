from django.urls import path
from . import views

app_name= 'surveys'

urlpatterns = [
    path('post/ajax/', views.submit_survey, name='submit_survey'),
    path('post/newsletter/', views.post_newsletter_email, name='post_newsletter_email'),


]
