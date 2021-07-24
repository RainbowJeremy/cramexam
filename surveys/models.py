from django.conf import settings
from django.db import models
from django.db.models.fields import DateField, EmailField
from django.template.defaultfilters import default, slugify

class Survey(models.Model):
    title = models.CharField(default='hello world', max_length=50)
    #placeholder = models.CharField(default='hello world', max_length=50)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) #make sure to make an anonymous user to reference.
    answer = models.CharField(max_length=20000, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        title = self.title
        self.slug = slugify(title)
        super(Survey, self).save(*args, **kwargs)

class Newsletter(models.Model):
    email = models.EmailField(max_length=25)

    def __str__(self):
        return self.email
