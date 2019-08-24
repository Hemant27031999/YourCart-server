from django.shortcuts import render
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from base_tech.forms import SignUpForm

# Create your views here.

def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')


def signup(request):
    print("Inside signup")
    if request.method == 'POST':
        print("Inside POST")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("form Valid")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            print("form invalid")
    else:
        print("Not POST")
        form = SignUpForm()
    return render(request, 'base_tech/signup.html', {'form': form})
