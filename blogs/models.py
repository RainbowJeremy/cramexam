from django.db import models
from django.db.models.fields import DateField
from django.template.defaultfilters import default, slugify

import re

class Article(models.Model):
    title = models.CharField(default='article-name', max_length=50)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=True)
    image = models.ImageField(null=True, upload_to='blog-images')
    text = models.CharField(max_length=10000, null=True, blank=True)
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        title = self.title
        self.slug = slugify(title)
        super(Article, self).save(*args, **kwargs)
 