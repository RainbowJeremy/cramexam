from django.db import models
from django.db.models.fields import DateField
from django.template.defaultfilters import default, slugify
from algorithms.pdf_reader import lect2vec
import re

class Lecture(models.Model):
    name = models.CharField(default='hello world', max_length=50)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=True)
    lecture = models.FileField(null=True, upload_to='lectures')
    text = models.CharField(max_length=20000, null=True, blank=True)
    
    def __str__(self):
        return re.search("\\\\(\w+\.\w{3,4}$)", self.lecture.path).group(1)
        
    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super(Lecture, self).save(*args, **kwargs)
        self.text = lect2vec(self.lecture.path)
        super(Lecture, self).save(*args, **kwargs)
        



class Question(models.Model):
    name = models.CharField(default='hello world', max_length=50)
    question = models.CharField(default='questionjnjifd', max_length=150)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=True)
    correct_answer = models.CharField(default='A', max_length=10)
    

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super(Question, self).save(*args, **kwargs)



class Answer(models.Model):
    author = models.CharField(default='hello world', max_length=50)
    date = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question, default=1, on_delete=models.CASCADE)
    text = models.CharField(default='hello world', max_length=250)
    is_selected = models.CharField(null=True, max_length=1)
    letter_key = models.CharField(default='A', max_length=1)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)


        #######################


        
