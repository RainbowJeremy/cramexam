from mcqgenerator.custom_views import DetailFormView, DetailFormSet
from django.db.models import fields
from django.urls import reverse
from django.shortcuts import render, redirect
from django.forms.models import BaseModelFormSet
from django.forms import formset_factory, inlineformset_factory
from .models import Lecture, Question, Answer
from .forms import LectureModelForm, QuestionModelForm, AnswerForm, PostLectureForm
from django.shortcuts import HttpResponseRedirect, HttpResponse
from amplitude import Amplitude
import re
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from blogs.models import Article
from surveys.models import Survey
from surveys.forms import SurveyModelForm

from django.core.paginator import Paginator

from algorithms import LatentDirichlet as LDA

from functools import wraps
import json




def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def record_event_data(request, event_name):
    amplitude = Amplitude()
    event_data = amplitude.build_event_data(
        event_type=event_name,
        request=request,
        app_version='1.0.0',
    )
    amplitude.send_events([event_data])


def file_drop(request):
    if request.method == 'POST':
        form = LectureModelForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            lecture = form.save()   #<first
            print("lecture.id: " + str(lecture.id))
            #record_event_data(request, 'lecture_submitted')
            #return HttpResponseRedirect(reverse('questions', id=lecture.id)) <- make this work later
            return redirect('/questions/'+ str(lecture.id) +'/')
    else:
        form = LectureModelForm()
        
    form = LectureModelForm()

    article_list = Article.objects.all()
    paginator = Paginator(article_list, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    survey_question = Survey.objects.all()[0]
    survey = SurveyModelForm(instance=survey_question)
    return render(request, 'file_drop.html', {'form': form, 'articles': articles, 'survey': survey})

###########################

def post_lecture(request):
    print(request.POST)
    if request.method == 'POST':
        form = PostLectureForm(request.POST)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            
            lecture = form.save()   #<first
            print("lecture.id: " + str(lecture.id))
            #record_event_data(request, 'lecture_submitted')
            #return HttpResponseRedirect(reverse('questions', id=lecture.id)) <- make this work later
            #return redirect('/questions/'+ str(lecture.id) +'/')
        else:
            print("is NOT VALID")


def handle_thebeast(lecture_text):
    mcq_finder = LDA.TheBeast(lecture_text)
    q_indices = mcq_finder.run()
    questions = Question.objects.filter(id__in=q_indices).exclude(question = 'nan')
    for q in questions:
        if q.question =='nan':
            print("got a nan")

    return questions


def questions(request, pk):
    uploaded_lect = Lecture.objects.filter(id=pk)[0]
    questions = handle_thebeast(uploaded_lect.text)
    record_event_data(request, 'landed_on_question_page')
    #questions = Question.objects.filter(id__in=[3,4,5,6,7,8]).exclude(question = 'nan')  # <- remove l8r
    question_set =[]
    for question in questions:
        answer_options=[]
        for answer in question.answer_set.all():
            if answer.text != 'nan':
                answer_options.append(AnswerForm(instance=answer))                
        question_set.append((question, answer_options))

    messages.add_message(request, messages.SUCCESS, 'Saved to Question Bank!')
    context={'uploaded_lect': uploaded_lect, 'question_set': question_set}
    return render(request, 'questions.html', context)



def postQuestion(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        print("GOT IT")
        print(request.POST)
        record_event_data(request, 'answered_question')
        post_dict ={}
        for k,v in request.POST.items():
            key = re.sub("form-\d{1,4}-", "", k)
            post_dict[key]=v
            
        
        related_q_pk = post_dict.pop("question-pk-input")
        related_question = Question.objects.filter(id=related_q_pk)[0]
        post_dict.update({'question':related_question})

        q_choices = related_question.answer_set.all()
        print(post_dict)
        for choice in q_choices:
            if post_dict['is_selected'] == choice.letter_key:
                form = AnswerForm(post_dict, instance=choice)
                break
        
        # save the data and after fetch the object in instance
        if form.is_valid():
            print("IS_ valid")
            instance = form.save()
            print("instance: "+str(instance))
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            print("IS not_ valid: "+ str(form.errors))
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

from django.contrib.auth import views as auth_views

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        import json 
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        json = json.dumps({ 'not_authenticated': True })
        return HttpResponse(json)
    
    wrapper.__doc__ = view_func.__doc__
    wrapper.__name__ = view_func.__name__ 
    return wrapper





@ajax_login_required
def question_bank(request):
    questions = Question.objects.filter(id__in=[3,4,5,6,7,8]).exclude(question = 'nan')  # <- remove l8r
    question_set =[]
    for question in questions:
        answer_options=[]
        for answer in question.answer_set.all():
            if answer.text != 'nan':
                answer_options.append(AnswerForm(instance=answer))                
        question_set.append((question, answer_options))

    context={'question_set': question_set}
    return render(request, 'questionbank.html', context)


