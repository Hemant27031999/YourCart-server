from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.middleware.csrf import get_token
from base_tech.forms import *
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
import io
from math import cos, asin, sqrt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import itertools


# Create your views here.


#DEFAULT page
def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')



#Sending CSRF Token
def getaccess(request):
    return JsonResponse({'csrfToken': get_token(request)})


# @method_decorator(csrf_exempt, name='dispatch')

#class SignUp1(APIView):
#    @csrf_exempt
#    def post(self, request):
#        serializer = UserCacheSerializer(data=request.data)
#        response = {'error': 'abc'}
#        if serializer.is_valid():
#            serializer.save()
#            print(serializer['phone_no'].value)
#            try:
#                obj = RegUser.objects.get(pk=serializer['phone_no'].value)
#                print(obj.first_name)
#                obj = UserCache.objects.get(phone_no=serializer['phone_no'].value)
#                obj.delete()
#                response = {'error': '', 'found': 'true' , 'phone_no': serializer['phone_no'].value, 'first_name': obj.first_name, 'email': obj.email, 'last_name': obj.last_name}
#            except :
#                print("hello")
#                response = {'error': '', 'found': 'false' , 'phone_no': serializer['phone_no'].value, 'first_name': '', 'email': '', 'last_name': ''}
#            return JsonResponse(response)
#        return JsonResponse(serializer.errors)
#
def signup1(request):
    if request.method == 'POST':
        no = request.POST['phone_no'];
        try:
            obj = RegUser.objects.get(pk=no)
            print(obj.first_name)
            response = {'error': '', 'found': 'true' , 'phone_no': no, 'first_name': obj.first_name, 'email': obj.email, 'last_name': obj.last_name}
        except :
            print("hello")
            response = {'error': '', 'found': 'false' , 'phone_no': no, 'first_name': '', 'email': '', 'last_name': ''}
        return JsonResponse(response)

#Regitering user
#def signup(request):
#    print("Inside signup")
#    response = JsonResponse({'Error': 'True'})
#    if request.method == 'POST':
#        print("Inside POST")
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            response = JsonResponse({'Error': 'False'})
#            print("form Valid")
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            logging_in_user = User.objects.get(username=username)
#            response = {'username' : logging_in_user.username, 'email' : logging_in_user.email, 'first_name' : logging_in_user.first_name, 'last_name' : logging_in_user.last_name, 'password1' : logging_in_user.password, 'password2' : logging_in_user.password}
#            return JsonResponse(response)
#        else:
#            print("form invalid")
#    else:
#        print("Not POST")
#        form = SignUpForm()
#        return render(request, 'base_tech/signup.html', {'form': form})
#    return JsonResponse({'credentials' : 'invalid'})


class SignUp(APIView):
    def post(self, request):
        print("Inside signup")
        response = JsonResponse({'Error': 'True'})
       # user = RegUser()
        print("Inside POST")
    #    user.first_name = request.POST.get('firstname')
    #    user.last_name = request.POST.get('lastname')
    #    user.password = request.POST.get('password')
    #    user.email = request.POST.get('emailid')
    #    user.phone_no = request.POST.get('phone')
    #    user.save()
    #    response = {'email' : user.email, 'first_name' : user.first_name, 'last_name' : user.last_name, 'password' : user.password, 'phone': user.phone_no}
        serializer = RegUserSerializer(data=request.data)
        response = {'success': 'false', 'error': 'invalid data'}
        if serializer.is_valid():
            serializer.save()
            email_err = ""
            phone_err = ""
            err_msg = { 'phone_no': phone_err, 'email': email_err }
            response = {'success': 'true', 'error': err_msg}
            return JsonResponse(response)
        print(serializer.errors)
        try:
            email_err = serializer.errors['email'][0]
        except:
            email_err = ""
        try:
            phone_err = serializer.errors['phone_no'][0]
        except:
            phone_err = ""
        err_msg = { 'phone_no': phone_err, 'email': email_err }
        response = {'success': 'false', 'error': err_msg}
        return JsonResponse(response)



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

def distance(lat1, lon1, lat2, lon2):
     p = 0.017453292519943295
     a = 0.5 - cos((lat2-lat1)*p)/2+cos(lat1*p)*cos(lat2*p)*(1-cos((lon2-lon1)*p))/2
     print(12742*asin(sqrt(a)))
     return 12742*asin(sqrt(a))

def unique(list1):

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


def useid(request, image_id):

    path = "%s"
    img = open(path, 'rb')
    response = FileResponse(img)
    return response

def get_products_cell(id)
{
    vendor_list = Cells.objects.filter(Cell_id = id)
    myProducts = set()
    for vendor in vendor_list:
        products = Vendor_Products.objects.filter(vendor_phone = vendor)
        for product in products:
            obj = CategorizedProducts.objects.filter(product_id = product.product_id)

            myProducts.add(obj[0].product_name)
            #myProducts.add(list1)
    return list(myProducts)
}

def is_Sublist(l, s):
	sub_set = False
	if s == []:
		sub_set = True
	elif s == l:
		sub_set = True
	elif len(s) > len(l):
		sub_set = False

	else:
		for i in range(len(l)):
			if l[i] == s[0]:
				n = 1
				while (n < len(s)) and (l[i+n] == s[n]):
					n += 1

				if n == len(s):
					sub_set = True

	return sub_set


def vendor_assignment(vendors,ar1,ar2):
    if len(vendors) == 0:
        remaining = list(zip(ar1,ar2))
        return remaining
    n = len(ar1)
    product_count = []
    for vendor in vendors:
        products_vendor = Vendor_Products.objects.filter(vendor_phone = vendor)
        myProducts=[]
        for product in products_vendor:
            obj = CategorizedProducts.objects.filter(product_id = product.product_id)
            myProducts.append(obj[0].product_name)
        m = len([value for value in ar1 if value in myProducts])
        product_count.append(m)
    zipped_pairs = zip(product_count,vendors)
    sorted_vendors = [x for _, x in sorted(zipped_pairs, reverse = True)]
    product_count = sorted(product_count, reverse = True)
    #check whether vendor accepts the order
    #vendor returns list which order he wants to accept
    accepted_orders=[]
    remaining_orders = [i for i in ar1 + accepted_orders if i not in accepted_orders]

    if len(remaining_orders)==0:
        empty =[]
        return empty

    # products_selected_vendor = (Vendor_Products.objecs.filter(vendor_phone = sorted_vendors[assigned_index]))
    # myProducts=[]
    # for product in products_vendor:
    #     obj = CategorizedProducts.objects.filter(product_id = product.product_id)
    #     myProducts.append(obj[0].product_name)

    vendors.remove(sorted_vendors[0])
    #new_ar1 = [i for i in ar1 + myproducts if i not in myproducts]
    new_ar1_vendor=ar1
    new_ar2_vendor=ar2
    for i in range(0,len(ar1)):
        if ar1[i] in accepted_orders:
            new_ar1_vendor.remove(new_ar1_vendor[i])
            new_ar2_vendor.remove(new_ar2_vendor[i])

    vendor_assignment(vendors, new_ar1_vendor, new_ar2_vendor)




def cell_sort(cells,product_count,ar1,ar2, user_address):
    if len(cells) == 0:
        remained = list(zip(ar1,ar2))
        return remained
    n = len(ar1)
    for cell in cells:
        products = get_products_cell(cell.Cell_id)
        m = len([value for value in ar1 if value in products])
        #m = number of required products cell has
        product_count.append(m)
    zipped_pairs = zip(product_count,cells)
    sorted_cells = [x for _, x in sorted(zipped_pairs, reverse = True)]
    product_count = sorted(product_count, reverse = True)
    flag = 0
    min_distance = 1000
    for i in range(0,product_count.count(product_count[0])):
        dist = distance(sorted_cells[i].Cell_lat,sorted_cells[i].Cell_long,user_address[0].latitude, user_address[0].longitude)
        if min_distance > dist:
            min_distance = dist
            closest_cell = sorted_cells[i].Cell_id
    # vendors
    vendors = list(Vendors.objects.filter(cell = closest_cell))
    remaining = vendor_assignment(vendors,ar1,ar2)

    if len(remaining)==0:
        empty = []
        return  empty

    new_ar1,ar2 = zip(*remaining)
    product_count = []
    #products = get_products_cell(closest_cell)
    #new_ar1 = [i for i in ar1 + products if i not in products]
    # for i in range(0,len(ar1)):
    #     if ar1[i] in myProducts:
    #         new_ar1.remove(myProducts[i])
    #         ar2.remove(new_ar2_vendor[i])
    cells.remove(closest_cell)
    cell_sort(cells, product_count , new_ar1,ar2, user_address)




def place_order(request):

    if request.method == 'POST':
#<<<<<<< HEAD
      #  order = Orders()
      #  order.item = request.POST['item']
      #  order.quantity = request.POST['quantity']
#=======
        print(request.POST)
        ar1 = request.POST.getlist('items')
        ar2 = request.POST.getlist('quantities')
        user = RegUser.objects.filter(phone_no = request.POST['phone_no'])
        user_address = Addresses.objects.filter(phone_no = user)
        print(request.POST.getlist('items'))

        i=0
        cells = list(Cells.objects.filter(city = user_address[0].city))
        product_count = []
        remaining_items = cell_sort(cells,product_count,ar1,ar2, user_address)


            # products = get_products_cell(cell.Cell_id)
            # if is_Sublist(products,ar1):
            #     flag = 1
            #     dist = distance(cell.Cell_lat,cell.Cell_long,user_address.latitude, user_address.longitude)
            #     if min_distance > dist:
            #         min_distance = dist
            #         closest_cell = cell.Cell_id


        #
        # if flag==1:
        #     vendors = Vendors.objects.filter(cell = closest_cell)
        #     for vendor in vendors:
        #         products_vendor = Vendor_Products.objecs.filter(vendor_phone = vendor)
        #         myProducts=[]
        #         for product in products_vendor:
        #             obj = CategorizedProducts.objects.filter(product_id = product.product_id)
        #
        #             myProducts.append(obj[0].product_name)
        #         if is_Sublist(products,ar1):
        #             closest_vendor = vendor
        #             break
        if remaining_items==0:
            for a,b in zip(ar1,ar2):
                if i==0:
                    obj = Orders.objects.create(phone_no = RegUser.objects.get(phone_no=request.POST['phone_no']), address = request.POST['address'], product_id = a, quantity = b)
                    order_id = obj.order_id
                    i=i+1
                else:
                    Orders.objects.create(phone_no = RegUser.objects.get(phone_no=request.POST['phone_no']), address = request.POST['address'], product_id = a, quantity = b, order_id= order_id)
                    i=i+1
          #      obj.order_id = request.POST['order_id']
          #      obj.phone_no = RegUser.objects.get(phone_no=request.POST['phone_no'])
          #      obj.address1 = request.POST['address']
          #      obj.product_id = a
          #      obj.quantity = b
          #      obj.save()
            response = {{'success': 'true'}}

            return JsonResponse(response)
        else:
            response = {{'success': 'true'},{"left":remaining}}
            return JsonResponse(response,safe=False)

      #  order = Orders()
      #  order.item = request.POST['item']
      #  order.quantity = request.POST['quantity']

#class Place_Orders(APIView):
#    def post(self, request):
#        serializer = OrdersSerializer(data=request.data)
#        response = {'error': 'abc'}
#        if serializer.is_valid():
#            print(serializer['product_id'])
#            for (a, b) in zip(serializer['items'].value, serializer['quantities'].value)
#                obj = Orders()
#                obj.order_id = serializer['order_id'].value
#                obj.phone_no = serializer['phone_no'].value
#                obj.address = serializer['address'].value
#                obj.product_id = a
#                obj.quantity = b
#                obj.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.errors)
#>>>>>>> 69cc78c39b13022ce36ebd5835e6c98cc72efb13





def save_address(request):

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            obj = Addresses2()
            obj.house_no = form.cleaned_data['house_no']
            obj.street = form.cleaned_data['street']
            obj.city = form.cleaned_data['city']
            obj.landmark = form.cleaned_data['landmark']
            obj.pincode = form.cleaned_data['pincode']
            obj.phone_no = form.cleaned_data['phone']
            obj.save()
            response = {'house_no': obj.house_no, 'street': obj.street, 'city': obj.city, 'landmark': obj.landmark, 'pincode': obj.pincode, 'phone_no': obj.phone}
            return JsonResponse(response)
        else:
            return JsonResponse({'Error': 'Invalid address !!!'})
    else:
        addresses = Addresses.objects.get(phone_no=request.GET['username'])
        myAddresses = []
        for address in addresses:
            dict = {}
            dict["house_no"] = product.house_no
            dict["street"] = product.street
            dict["city"] = product.city
            dict["landmark"] = product.landmark
            dict["pincode"] = product.pincode
            dict["address_id"] = product.address_id
            dict["phone_no"] = product.phone_no
            myAddresses.append(dict)

        return JsonResponse({'addresses' : myAddresses})



class save_address(APIView):
    def post(self,request):
        response = JsonResponse({'Error': 'True'})
        add_serializer = RegAddresses(data=request.data)
        if add_serializer.is_valid():
            add_serializer.save()
            return JsonResponse(add_serializer.data)
        return JsonResponse(add_serializer.errors)

class get_address(APIView):
    def post(self,request):
        address=(list(Addresses.objects.filter(phone_no=request.POST['phone_no']).values()))
        #address = get_object_or_404(Addresses,phone_no=request.GET.get('phone_no'))
        #print(address)
        #hello={"hello":"12"}
        return JsonResponse(address,safe=False)






def get_products(request):
    if request.method == "POST":
        mlong = float(request.POST['longitude'])
        mlat = float(request.POST['latitude'])
        mcity = request.POST['city']

        vendors = Vendors.objects.filter(city = mcity)
        print(vendors)
        selected_vendors = []
        myProducts = []


        for vendor in vendors:
            print(type(mlat))
            if(distance(mlat, mlong, vendor.vendor_lat, vendor.vendor_long) < 7):
                selected_vendors.append(vendor)


        for vendor in selected_vendors:
            products = Vendor_Products.objects.filter(vendor_phone = vendor)
            #products = (vendor.products.all())
            #print(products.product_id)

            for product in products:
                obj = CategorizedProducts.objects.filter(product_id = product.product_id)
                d = {}
                d["under_category"]=obj[0].under_category.categoryName
                d["product_name"]=obj[0].product_name
                d["product_id"]=obj[0].product_id
                d["product_price"]=obj[0].product_price
                d["product_rating"]=obj[0].product_rating
                d["product_descp"]=obj[0].product_descp
                d["product_imagepath"]=obj[0].product_imagepath
                #y = json.loads(d.replace("\"",''))
                #list1=[]

                myProducts.append((d))
                #myProducts.add(list1)
        myProducts=unique(myProducts)
        print(myProducts)
        dict={"Prod":(myProducts)}
        #print(myProducts)
        #dict={"Prod":"13"}
        #print(JsonResponse((myProducts),safe=False))


        return JsonResponse(dict, safe=False)


    else:
        return JsonResponse({'error' : 'Not a POST request'})
