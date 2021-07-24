from surveys.models import Survey
from django.contrib import admin
from .models import Newsletter, Survey
# Register your models here.
admin.site.register(Survey)
admin.site.register(Newsletter)