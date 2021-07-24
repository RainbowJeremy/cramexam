from django.db import models
from django.contrib.auth.models import User
from mcqgenerator.models import Question



class Profile(models.Model):
    #GDPR_CHOICES = (("I agree","Y"), ("I don't agree","N"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    questions = models.ManyToManyField(Question)

    

    def __str__(self):
        return f'{self.user.username} Profile'
