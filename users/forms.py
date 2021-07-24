from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']