from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from base_tech.forms import SignUpForm
from django.contrib.auth.models import User

# Create your views here.


#DEFAULT page
def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')



#Sending CSRF Token
def getaccess(request):
    return JsonResponse({'csrfToken': get_token(request)})



#Regitering user
def signup(request):
    print("Inside signup")
    response = JsonResponse({'Error': 'True'})
    if request.method == 'POST':
        print("Inside POST")
        form = SignUpForm(request.POST)
        if form.is_valid():
            response = JsonResponse({'Error': 'False'})
            print("form Valid")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            logging_in_user = User.objects.get(username=username)
            response = {'username' : logging_in_user.username, 'email' : logging_in_user.email, 'first_name' : logging_in_user.first_name, 'last_name' : logging_in_user.last_name, 'password1' : logging_in_user.password, 'password2' : logging_in_user.password}
            return JsonResponse(response)
        else:
            print("form invalid")
    else:
        print("Not POST")
        form = SignUpForm()
        return render(request, 'base_tech/signup.html', {'form': form})
    return JsonResponse({'credentials' : 'invalid'})



#Signing in User
def loginuser(request):
    print("Inside login")

    if request.method == 'POST':
        print("Inside POST")
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            logging_in_user = User.objects.get(username=username)
            response = {'username' : logging_in_user.username, 'email' : logging_in_user.email, 'first_name' : logging_in_user.first_name, 'last_name' : logging_in_user.last_name, 'password1' : logging_in_user.password, 'password2' : logging_in_user.password}
            return JsonResponse(response)
        else:
            return JsonResponse({'Error': 'Error Signing in !!!'})
    else:
        print("Not POST")
        return JsonResponse({'Error': 'Not a post call !!!'})
