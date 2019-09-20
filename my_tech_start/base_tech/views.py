from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.middleware.csrf import get_token
from base_tech.forms import *
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
            # items = Category.objects.all()
            # myCategories = []
            # for item in items:
            #     dict = {}
            #     dict["categoryId"] = item.categoryId
            #     dict["categoryName"] = item.categoryName
            #     dict["categoryImagePath"] = item.categoryImagePath
            #     myCategories.append(dict)

            response = {'username' : logging_in_user.username, 'email' : logging_in_user.email, 'first_name' : logging_in_user.first_name, 'last_name' : logging_in_user.last_name}
            return JsonResponse(response)
        else:
            return JsonResponse({'Error': 'Error Signing in !!!'})
    else:
        print("Not POST")
        return JsonResponse({'Error': 'Not a post call !!!'})


def loadAllCategories(request):
    username = request.POST['username']
    if User.objects.filter(username=username):
        items = Category.objects.all()
        myCategories = []
        for item in items:
            dict = {}
            dict["categoryId"] = item.categoryId
            dict["categoryName"] = item.categoryName
            dict["categoryImagePath"] = item.categoryImagePath
            myCategories.append(dict)

        return JsonResponse({'categories' : myCategories})

    else:
        return JsonResponse({'categories' : []})


def loadSingleCategory(request, categoryId):
    products = CategorizedProducts.objects.filter(under_category=categoryId)
    myProducts = []
    for product in products:
        dict = {}
        dict["under_category"] = product.under_category
        dict["product_name"] = product.product_name
        dict["product_descp"] = product.product_descp
        dict["product_id"] = product.product_id
        dict["product_price"] = product.product_price
        dict["product_rating"] = product.product_rating
        dict["product_imagepath"] = product.product_imagepath
        myProducts.append(dict)

    return JsonResponse({'products' : myProducts})


def hotel_image_view(request):

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'base_tech/hotel_image_form.html', {'form' : form})


def success(request):
    return HttpResponse('successfuly uploaded')


def display_hotel_images(request):

    if request.method == 'GET':

        # getting all the objects of hotel.
        Hotels = Hotel.objects.all()
        print(Hotels[0].hotel_Main_Img.url)
        return render(request, 'base_tech/display_hotel_images.html',
                     {'hotel_images' : Hotels})


def send_file(response):

    img = open('media/images/Screenshot_from_2019-06-27_01-12-24.png', 'rb')
    response = FileResponse(img)
    return response


def useid(request, image_id):

    path = "%s"
    img = open(path, 'rb')
    response = FileResponse(img)
    return response
