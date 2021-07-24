from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import json 
from django.contrib.auth.views import LogoutView

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('pages:home')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)


def ajax_login(request):
    if request.method == 'POST':                                                                                                                                                                                                           
        login_form = AuthenticationForm(request, request.POST)
        response_data = {}                                                                              
        if login_form.is_valid():                                                                                                           
            response_data['success'] = 'true'
            intent = login_form.cleaned_data.get('intent')
            print("intent: " + str(intent))
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user) 
                response_data['message'] = 'You"re logged in'
        else:
            response_data['success'] = 'false'
            response_data['message'] = 'You messed up'  

         

        return HttpResponse(json.dumps(response_data), content_type="application/json")  



@login_required
def profile(request):
    if request == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(f'Your Account has been Updated!')
            redirect('profile')#???
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {'u_form':u_form, 'p_form':p_form}
    return render(request, 'profile.html', context)


