from django.contrib import admin
from .models import Lecture, Question, Answer

admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Answer)