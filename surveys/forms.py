from django import forms
from django.forms.widgets import RadioSelect
from .models import Survey, Newsletter

class SurveyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyModelForm, self).__init__(*args, **kwargs)
        #self.fields['answer'].label = self

    class Meta:
        model = Survey
        fields = ['answer']


class NewsletterModelForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'placeholder':'Email'}))

    def __init__(self, *args, **kwargs):
        super(NewsletterModelForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""

    class Meta:
        model = Newsletter
        fields = ['email']
