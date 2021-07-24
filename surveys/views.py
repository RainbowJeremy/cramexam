from mcqgenerator.views import question_bank
from django.shortcuts import render, redirect
from .forms import SurveyModelForm, NewsletterModelForm
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def submit_survey(request):
    print(request.POST)
    if request.method == 'POST':
        form = SurveyModelForm(request.POST)
        if form.is_valid():
            survey = form.save()   #<first
            print("survey.id: " + str(survey.id))
            #record_event_data(request, 'lecture_submitted')
        else:
            print("is NOT VALID")
            return redirect(reverse("mcqgenerator:file_drop"))

def post_newsletter_email(request):
    print(request.POST)
    if request.method == 'POST':
        form = NewsletterModelForm(request.POST)
        print(form)
        if form.is_valid():
            email = form.save()   #<first
            print("Newslette.id: " + str(email))
            #record_event_data(request, 'lecture_submitted')
            return HttpResponse('hello worl')
        else:
            print("is NOT VALID")
            return redirect(reverse("mcqgenerator:file_drop"))

def get_survey_dict(index=None):
    from surveys.models import Survey
    from surveys.forms import SurveyModelForm
    from random import random
    if not index:
        index = [1] #random.randint(1, )
    
    elif isinstance(index, int):
        index = [index]

    question = Survey.objects.filter(id__in=index)
    form = SurveyModelForm(instance= question)

    survey_dict = {'question':question, 'form':form}
    return survey_dict
    