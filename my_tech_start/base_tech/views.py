from django.shortcuts import render
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from base_tech.forms import SignUpForm

# Create your views here.

def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')

def getaccess(request):
    return JsonResponse({'csrfToken': get_token(request)})


def signup(request):
    print("Inside signup")
    response = JsonResponse({'Error': 'True'})
    if request.method == 'POST':
        print("Inside POST")
        # response = HttpResponse("Some error has occurred")
        form = SignUpForm(request.POST)
        if form.is_valid():
            response = JsonResponse({'Error': 'False'})
            print("form Valid")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return response
        else:
            print("form invalid")
    else:
        print("Not POST")
        form = SignUpForm()
        return render(request, 'base_tech/signup.html', {'form': form})
    return response
