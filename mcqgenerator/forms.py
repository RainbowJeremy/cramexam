from django import forms
from django.forms.widgets import RadioSelect
from .models import Lecture, Question, Answer

class LectureModelForm(forms.ModelForm):
    lecture = forms.FileField(widget=forms.FileInput(attrs={ 'class': "drop-zone__input", 
                                                            "name" :"myFile",
                                                            "type":"file", #" font-size: 1rem;",
                                                            "id": "file-id",
                                                            }))

    def __init__(self, *args, **kwargs):
        super(LectureModelForm, self).__init__(*args, **kwargs)
        self.fields['lecture'].label = ""

    class Meta:
        model = Lecture
        fields = ['lecture']

class PostLectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['text']

class OptionSelect(forms.RadioSelect):
    pass

class QuestionModelForm(forms.ModelForm):
    #answer_choices = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Lecture.objects.all())
    def __init__(self, *args, **kwargs):
        super(QuestionModelForm, self).__init__(*args, **kwargs)
        self.fields['answers']=forms.ModelChoiceField(queryset=Question.objects.all(), widget=OptionSelect) # get correct queryset, pass values down

    class Meta:
        model = Question
        fields = ['name', 'question', 'correct_answer']

class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['is_selected']=forms.ChoiceField(choices = [(self.instance.letter_key, self.instance.text)], widget=forms.RadioSelect(attrs={'class':'choice_div'})) 
        self.fields['is_selected'].label = self.instance.letter_key

    class Meta:
        model = Answer
        fields = ['is_selected']

