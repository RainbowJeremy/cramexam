from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Article

class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ArticleCreateView(AdminOnlyMixin, CreateView):
    model = Article
    fields = ['title','image','text']


class ArticleUpdateView(AdminOnlyMixin, UpdateView):
    model = Article
    fields = ['title','image','text']
    template_name_suffix = '_update_form'
