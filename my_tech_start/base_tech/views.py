from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from .models import *
from vendor_side.models import *
from .serializers import *
from rest_framework.response import Response
import io
from math import cos, asin, sqrt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import itertools
#from background_task import background
from vendor_side.views import *
from delivery_side.views import *
from django.utils import timezone
import datetime
import requests
from django.utils.safestring import mark_safe
import json
import requests
from geographiclib.geodesic import Geodesic
from copy import deepcopy
import uuid
import firebase_admin
import google
from firebase_admin import credentials,firestore

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


def user_list(request):
    return render(request, 'base_tech/abc.html', {})

# DEFAULT page
def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')


# Sending CSRF Token
def getaccess(request):
    return JsonResponse({'csrfToken': get_token(request)})


def initialsignup(request):
    if request.method == 'POST':
        no = request.POST['phone_no'];
        try:
            obj = RegUser.objects.get(pk=no)
            print(obj.first_name)
            response = {'error': '', 'found': 'true', 'phone_no': no, 'first_name': obj.first_name, 'email': obj.email,
                        'last_name': obj.last_name}
        except:
            print("hello")
            response = {'error': '', 'found': 'false', 'phone_no': no, 'first_name': '', 'email': '', 'last_name': ''}
        return JsonResponse(response)


class SignUp(APIView):
    def post(self, request):
        print("Inside signup")
        response = JsonResponse({'Error': 'True'})
        print("Inside POST")
        serializer = RegUserSerializer(data=request.data)
        response = {'success': 'false', 'error': 'invalid data'}
        if serializer.is_valid():
            serializer.save()
            email_err = ""
            phone_err = ""
            err_msg = {'phone_no': phone_err, 'email': email_err}
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
        err_msg = {'phone_no': phone_err, 'email': email_err}
        response = {'success': 'false', 'error': err_msg}
        return JsonResponse(response)


# Signing in User
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

            response = {'username': logging_in_user.username, 'email': logging_in_user.email,
                        'first_name': logging_in_user.first_name, 'last_name': logging_in_user.last_name}
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

        return JsonResponse({'categories': myCategories})

    else:
        return JsonResponse({'categories': []})


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

    return JsonResponse({'products': myProducts})




def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'base_tech/hotel_image_form.html', {'form': form})


def success(request):
    return HttpResponse('successfuly uploaded')


def display_hotel_images(request):
    if request.method == 'GET':
        Hotels = Hotel.objects.all()
        print(Hotels[0].hotel_Main_Img.url)
        return render(request, 'base_tech/display_hotel_images.html',
                      {'hotel_images': Hotels})


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

def get_products_cell(cell):
    vendor_list = Vendors.objects.filter(cell = cell)
    myProducts = set()
    for vendor in vendor_list:
        if vendor.current_no_orders < 5:
            products = Vendor_Products.objects.filter(vendor_phone = vendor)
            for product in products:
                myProducts.add(product.product_id)
                #myProducts.add(list1)
    return list(myProducts)


def get_order_history(request):
    objs = Orders.objects.filter(customer_phone=RegUser.objects.get(phone_no=request.POST['cust_phone'])).filter(status='Delivired')
    cust_orders = list(objs)
    no_orders = len(cust_orders)
    obj_list = []
    print(cust_orders)
    for i in range(no_orders):
        print(cust_orders[i].product_id.product_id)
        obj = CategorizedProducts.objects.get(product_id=cust_orders[i].product_id.product_id)
        prod = {
            'prod_id': obj.product_id,
            'prod_name': obj.product_name,
            'category_name': obj.under_category.categoryName,
            'category_id': obj.under_category.categoryId,
            'prod_price': obj.product_price,
            'prod_rating': obj.product_rating,
            'prod_desc': obj.product_descp,
            'prod_img': obj.product_imagepath,
            'check': False
        }
        obj_list.append(prod)
    data = {
        'no_prod': no_orders,
        'products': obj_list
    }
    return JsonResponse(data)


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


def vendor_assignment(vendors,ar1,ar2,vendor_assigned_list,accepted_orders_list,rejected_orders_list,order_id):
    print("a",vendors)
    if (len(vendors) == 0):
        print("len_vendors")
        print(ar1)
        print(ar2)
        return ar1,ar2,vendor_assigned_list,accepted_orders_list,rejected_orders_list
    if len(ar1)==0:
        return ar1,ar2
    n = len(ar1)
    product_count = []
    for vendor in vendors:
        products_vendor = Vendor_Products.objects.filter(vendor_phone = vendor)
        myProducts=[]
        for product in products_vendor:
            myProducts.append(product.product_id)
        m = len([value for value in ar1 if value in myProducts])
        product_count.append(m)
    print(product_count)
    
    cmax=0
    vmax=vendors[0]
    for count,ven in zip(product_count,vendors):
         if count>=cmax:
             cmax=count
             vmax=ven
    print("vendors_max",vmax)
    print("count_max",cmax)
    total_orders = []
    order_quantities = []
    
    products_selected_vendor = list(Vendor_Products.objects.filter(vendor_phone = vmax))
    myProducts=[]
    for product in products_selected_vendor:
        myProducts.append(product.product_id)
    
    for item,quan in zip(ar1,ar2):
        if item in myProducts:
            total_orders.append(item)
            order_quantities.append(quan)
    print(total_orders)

    #assuming for now
    accepted_orders = total_orders
    curr_no_orders = vmax.current_no_orders
    vmax.current_no_orders = curr_no_orders +1
    total_no_orders = vmax.total_no_orders
    vmax.total_no_orders = total_no_orders + 1
    vmax.save()
    send_vendor_order(order_id,vmax.phone_no, total_orders, order_quantities)
    #rejected orders
    rejected_orders = []
    for item in total_orders:
        if item not in accepted_orders:
            rejected_orders.append(item)
    post_data = {
        "total_orders" : accepted_orders,
        "order_quantities" : order_quantities,
        "Vendor_phone" : vmax.phone_no
    }

    vendor_assigned_list.append(vmax)
    accepted_orders_list.append(accepted_orders)
    rejected_orders_list.append(rejected_orders)

    print("rejected_orders////////",rejected_orders)

    vendors.remove(vmax)
    toremove_ar1=[]
    toremove_ar2=[]
    #new_ar1 = [i for i in ar1 + myproducts if i not in myproducts]
    for a,b in zip(ar1,ar2):
        if a in accepted_orders:
            toremove_ar1.append(a)
            toremove_ar2.append(b)
    for a,b in zip(toremove_ar1,toremove_ar2):
        ar1.remove(a)
        ar2.remove(b)

    print("end of v_assign",ar1)
    print(ar2)
    new1,new2,new_v_a_l,new_a_o_l,new_r_o_l=vendor_assignment(vendors, ar1, ar2,vendor_assigned_list, accepted_orders_list, rejected_orders_list,order_id)
    return new1,new2,new_v_a_l,new_a_o_l,new_r_o_l




def cell_sort(cells,product_count,ar1,ar2, user_latitude,user_longitude,city,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance_all,cell_distance,order_id):
    print("cell_sort_top",cells)
    if len(cells) == 0:
        print("len_cells=0")
        return ar1,ar2,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance
    if len(ar1)==0:
        print("len_ar1=0")
        return ar1,ar2,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance
    n = len(ar1)

    for cell in cells:
        products = get_products_cell(cell)
        print("products",products)
        m = len([value for value in ar1 if value in products])
        print("ar1",ar1)
        print("m",m)
        #m = number of required products cell has
        product_count.append(m)
    
    count_max=0
    cell_max_list=[]
    for count,cell in zip(product_count,cells):
         if count>count_max:
             count_max = count
             cell_max_list=[]
             cell_max_list.append(cell)
         elif count==count_max:
             cell_max_list.append(cell)
    print("vendors_max",cell_max_list)
    print("count_max",count_max)

    if count_max == 0:
        return ar1,ar2,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance


    min_distance = 1000
    for cell in cell_max_list:
        dist = distance(cell.Cell_lat,cell.Cell_long,user_latitude, user_longitude)
        if min_distance > dist:
            min_distance = dist
            closest_cell = cell
    p1=(get_products_cell(closest_cell))
    print([value for value in ar1 if value in p1])
    vendors = []
    print("closest_cell",closest_cell)
    vendors_all = list(Vendors.objects.filter(cell = closest_cell))
    for vendor in vendors_all:
        if vendor.current_no_orders < 5:
            vendors.append(vendor)
    valist=[]
    alist = []
    ralist = []
    new_ar1,new_ar2,valist,alist,ralist= vendor_assignment(vendors,ar1,ar2,valist,alist,ralist,order_id)
    vendor_assigned_list.append(valist)
    accepted_orders_list.append(alist)
    rejected_orders_list.append(ralist)

    print(new_ar1)
    print(new_ar2)


    product_count = []
    
    cell_distance.append(cell_distance_all[cells.index(closest_cell)])
    
    cell_distance_all.remove(cell_distance_all[cells.index(closest_cell)])
    cells.remove(closest_cell)
    new1,new2,new_valist,new_alist,new_ralist,cell_distance=cell_sort(cells, product_count , new_ar1,new_ar2, user_latitude,user_longitude,city,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance_all,cell_distance,order_id)
    return new1,new2,new_valist,new_alist,new_ralist,cell_distance

def get_bearing(lat1, lat2, long1, long2):
    brng = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1']
    return brng

def sector_check(lat1,long1,lat2,long2,lat3,long3):
    angle = get_bearing(lat1, lat2, long1, long2) - get_bearing(lat2, lat3, long2, long3)
    if(angle>=0):
        angle = 180 - angle
        return angle,0
    else:
        angle = -180 - angle
        return angle,1


def delivery_boy_assignment(vendor_assigned_list,cell_distance,user_latitude,user_longitude,city,phone_no,order_id):
    val_inside = []
    dist_inside = []
    min_u2d = 10000
    #distance_sector = []
    final_vendor_cell = []
    # final_aol = []
    final_deliverBoy = []
    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate("../serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db =firestore.client()
    deliveryBoy_list = list(Delivery_Boys.objects.filter(city__iexact = city,status="A",busy="False"))

    for boy in deliveryBoy_list:
        doc_rf=db.collection(u'DeliveryBoyLocation').document(u'{}'.format(boy.phone_no))
        doc=doc_rf.get()
        boy.lat = doc.to_dict()['geo_point'].latitude
        boy.long = doc.to_dict()['geo_point'].longitude
        boy.save()



    # city = city, ))
    checkpoint_lat = user_latitude
    checkpoint_long = user_longitude
    # , status = 'I',busy = False))
    print("deliveryBoy_list",deliveryBoy_list)
    min_checkpoint = 1000
    for val,dist in zip(vendor_assigned_list,cell_distance):
        print("dist",dist)
        if dist<0.5:
            if(dist<min_checkpoint):
                min_checkpoint = dist
                checkpoint_lat = val[0].cell.Cell_lat
                checkpoint_long = val[0].cell.Cell_long
            val_inside.append(val)
            print("val_inside",val_inside)
            dist_inside.append(dist)

            #distance_sector.append(dist)
    for val,dist in zip(val_inside,dist_inside):
        if val in vendor_assigned_list:
            vendor_assigned_list.remove(val)
            cell_distance.remove(dist)

    print("inside",val_inside)
    if(vendor_assigned_list==[]):
        ##bacha hai
        max_distance =0
        for v1,d1 in zip(val_inside,dist_inside):
            if(d1>=max_distance):
                farthest_cell = v1
                max_distance = d1


        firstmin = deliveryBoy_list[0]
        secmin = deliveryBoy_list[0]
        thirdmin = deliveryBoy_list[0]
        for i in range(0, len(deliveryBoy_list)):

            if distance(deliveryBoy_list[i].lat,deliveryBoy_list[i].long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long) < distance(firstmin.lat,firstmin.long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long):
                thirdmin = secmin
                secmin = firstmin
                firstmin = deliveryBoy_list[i]

            if distance(deliveryBoy_list[i].lat,deliveryBoy_list[i].long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long) < distance(firstmin.lat,firstmin.long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long):
                thirdmin = secmin
                secmin = deliveryBoy_list[i]
            if distance(deliveryBoy_list[i].lat,deliveryBoy_list[i].long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long) < distance(firstmin.lat,firstmin.long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long):
                thirdmin = deliveryBoy_list[i]

        val_name=[]
        val_address= []
        val_lat = []
        val_long = []
        for ven_l in val_inside:
            for ven in ven_l:
                val_name.append(ven.name)
                val_address.append(ven.address)
                val_lat.append(ven.vendor_lat)
                val_long.append(ven.vendor_long)
        primaryBoy = firstmin
        print("firstmin",primaryBoy)
        data = {
            "order_id":str(order_id),
            "vendor_name":val_name,
            "vendor_address":val_address,
            "vendor_lat":val_lat,
            "vendor_long":val_long,
            "checkpoint_lat": checkpoint_lat,
            "checkpoint_long":checkpoint_long,
            "user_latitude":user_latitude,
            "user_longitude":user_longitude,
            "user_phone":phone_no,
            "split":False,
            "isprimary":True
        }
        send_delivery_order(data,primaryBoy.phone_no)
        
    count_sector = 0



    for vendor_cell,dist in zip(reversed(vendor_assigned_list),reversed(cell_distance)):
        # if vendor_cell in final_vendor_cell:
        #     continue
        count_sector=count_sector+1
        print("vendor_cell",vendor_cell)
        vendor_assigned_list.remove(vendor_cell)
        cell_distance.remove(dist)
        max_u2c = dist
        farthest_cell= vendor_cell

        vendor_cell_sector = []
        pos_v = []
        neg_v=[]
        pos_d=[]
        neg_d=[]

        for v1,d1 in zip(reversed(vendor_assigned_list),reversed(cell_distance)):
            # if (v1 not in final_vendor_cell):
            #     if v1!=vendor_cell:
            print("v1",v1)
            cell = v1[0].cell
            angle,sign = sector_check(vendor_cell[0].cell.Cell_lat,vendor_cell[0].cell.Cell_long,user_latitude,user_longitude,cell.Cell_lat,cell.Cell_long)
            print("angle",angle)
            print("sign",sign)
            if abs(angle)<30:
                if sign==0:
                    pos_v.append(v1)
                    pos_d.append(d1)
                else:
                    neg_v.append(v1)
                    neg_d.append(d1)
        if len(pos_v)>len(neg_v):
            for v1,d1 in zip(pos_v,pos_d):
                print("inside if_poslen",v1)
                vendor_cell_sector.append(v1)
                vendor_assigned_list.remove(v1)
                cell_distance.remove(d1)
                
                if(d1>max_u2c):
                    max_u2c = d1
                    farthest_cell = v1


        else:
            for v1,d1 in zip(pos_v,pos_d):
                print("inside if_neglen",v1)
                vendor_cell_sector.append(v1)
                vendor_assigned_list.remove(v1)
                cell_distance.remove(d1)
                
                if(d1>max_u2c):
                    max_u2c = d1
                    farthest_cell = v1
        print("vendor_cell_sector",vendor_cell_sector)



        min = 10000
        for boy in deliveryBoy_list:
            d = distance(boy.lat,boy.long,farthest_cell[0].cell.Cell_lat,farthest_cell[0].cell.Cell_long)
            if(d < min):
                min = d
                closestBoy = boy

        print(closestBoy)
        print("dist+min",dist+min)
        if (dist+min)<min_u2d:
            min_u2d = (dist+min)
            print("min_u2d",min_u2d)
            primaryBoy = closestBoy
        for vcs in vendor_cell_sector:
            final_deliverBoy.append(closestBoy)
            final_vendor_cell.append(vcs)

        final_deliverBoy.append(closestBoy)
        final_vendor_cell.append(vendor_cell)
        deliveryBoy_list.remove(closestBoy)
    print(primaryBoy)
    for v1 in val_inside:
        final_vendor_cell.append(v1)
        final_deliverBoy.append(primaryBoy)
    if val_inside==[]:
        checkpoint_lat = user_latitude
        checkpoint_long = user_longitude
    print(final_vendor_cell)
    print(final_deliverBoy)
    unique_deliver_boy = unique(final_deliverBoy)
    for boy in unique_deliver_boy:
        indices = [i for i, x in enumerate(final_deliverBoy) if x == boy]
        vendor_list = []
        vendor_address = []
        vendor_lat = []
        vendor_long = []
        for index in indices:
            for ven in final_vendor_cell[index]:
                vendor_list.append(ven.name)
                vendor_address.append(ven.address)
                vendor_lat.append(ven.vendor_lat)
                vendor_long.append(ven.vendor_long)
        if boy==primaryBoy:
            isprimary = True
        else:
            isprimary = False
        data = {
            "order_id": str(order_id),
            "vendor_name":vendor_list,
            "vendor_address":vendor_address,
            "vendor_lat":vendor_lat,
            "vendor_long":vendor_long,
            "checkpoint_lat": checkpoint_lat,
            "checkpoint_long":checkpoint_long,
            "user_latitude":user_latitude,
            "user_longitude":user_longitude,
            "user_phone":phone_no,
            "split":count_sector>1,
            "isprimary":isprimary
        }
        print("boy",boy)
        send_delivery_order(data,boy.phone_no)
        # print("data",data)



    print("checkpoint: ",checkpoint_lat ," ",checkpoint_long )
    return final_vendor_cell,final_deliverBoy,primaryBoy


def place_order(request):
    if request.method == 'POST':
        order_id = uuid.uuid4()
        print(order_id)
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print(body)
        items = body['items']
        city = body['city']
        user_latitude = float(body['order_lat'])
        user_longitude = float(body['order_long'])
        print(items)

        ar1 =[]
        ar2=[]
      #  print(request.POST.getlist('items'))
        for item in items:
            prodid = int(item['productid'])
            itemcount = int(item['itemcount'])
            ar1.append(prodid)
            ar2.append(itemcount)
        print(ar1)
        print(ar2)
        

        i=0
        #cells = list(Cells.objects.filter(city__iexact = city))
        cells_all = list((Cells.objects.filter(city__iexact = city)))
        cells = []
        cell_distance_all = []
        cell_distance = []
        for cell in cells_all:
            d = (distance(user_latitude,user_longitude , cell.Cell_lat, cell.Cell_long))
            #distance problem
            if d<=7:
                cells.append(cell)
                cell_distance_all.append(d)
        print(cells)
        product_count = []
        vendor_assigned_list=[]
        accepted_orders_list=[]
        rejected_orders_list=[]
        ar1_rem,ar2_rem,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance = cell_sort(cells,product_count,deepcopy(ar1),deepcopy(ar2), user_latitude,user_longitude,city,vendor_assigned_list,accepted_orders_list,rejected_orders_list,cell_distance_all,cell_distance,order_id)
        print(vendor_assigned_list)
        print(accepted_orders_list)
        print(rejected_orders_list)
        print(cell_distance)
        if vendor_assigned_list != []:
            final_vendor_cell,final_deliverBoy,primaryBoy=delivery_boy_assignment(deepcopy(vendor_assigned_list),deepcopy(cell_distance),user_latitude,user_longitude,city,body['phone_no'],order_id)

            
        print(ar1)
        i=0
        if ar1_rem==[]:

            print(order_id)
            for cell,cell_accepted_order,cell_rejected_order in zip(vendor_assigned_list,accepted_orders_list,rejected_orders_list):
                for ven,ven_accepted_order,ven_rejected_order in zip(cell,cell_accepted_order,cell_rejected_order):
                    for ven_order in ven_accepted_order:
                        delivery_boy_phone = final_deliverBoy[final_vendor_cell.index(cell)]
                        if delivery_boy_phone==primaryBoy:
                            value = "P"
                        else:
                            value = "S"
                        obj = CategorizedProducts.objects.filter(product_id = ven_order)
                        Orders.objects.create(
                            customer_phone=RegUser.objects.get(phone_no=body['phone_no']),
                            address=body['address'],
                            product_id=obj[0],
                            quantity=ar2[ar1.index(ven_order)],
                            order_id=order_id,
                            delivery_boy_phone = final_deliverBoy[final_vendor_cell.index(cell)],
                            delboy_type = value,
                            vendor_phone=ven.phone_no,
                            cust_lat=user_latitude,
                            cust_long=user_longitude
                        )

                        prev_orders.objects.create(order_id = order_id, vendor_phone = ven.phone_no ,product_id = obj[0], status = "A")
                    for ven_order in ven_rejected_order:
                        prev_orders.objects.create(order_id = order_id, vendor_phone = ven.phone_no ,product_id = obj[0], status = "R")

            response = {
         #       'success': 'true',
                'primaryBoy_name':primaryBoy.name,
                'primaryBoy_phone':primaryBoy.phone_no
            }

            return JsonResponse(response)
        else:
            response = {'success': 'False',"left_prod":ar1_rem,"left_quan":ar2_rem}
            return JsonResponse(response,safe=False)

def subscribe_order(request):
    if request.method == 'POST':
        print(request.POST)
        ar1 = request.POST.getlist('items')
        ar2 = request.POST.getlist('quantities')
        print(request.POST.getlist('items'))
        dates = "[ "
        for d in request.POST['dates']:
            date = str(d)
            date.join(" ")
            dates.join(date)
        dates.join("]")
        months = "[ "
        for m in request.POST['months']:
            month = str(m)
            month.join(" ")
            months.join(month)
        months.join("]")
        i = 0
        for a, b in zip(ar1, ar2):
            if i == 0:
                obj = Subscribed_Orders.objects.create(
                    customer_phone=RegUser.objects.get(phone_no=request.POST['phone_no']),
                    address=request.POST['address'],
                    product_id=a,
                    quantity=b,
                    delivery_dates=dates,
                    delivery_months=months,
                    delivery_time=request.POST['del_time'],
                )
                order_id = obj.sorder_id
                i = i + 1
            else:
                Subscribed_Orders.objects.create(
                    customer_phone=RegUser.objects.get(phone_no=request.POST['phone_no']),
                    address=request.POST['address'],
                    product_id=a,
                    quantity=b,
                    sorder_id=order_id,
                    delivery_dates=dates,
                    delivery_months=months,
                    delivery_time=request.POST['del_time'],
                )
                i = i + 1
        response = {'success': 'true'}

        return JsonResponse(response)

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
            response = {'house_no': obj.house_no, 'street': obj.street, 'city': obj.city, 'landmark': obj.landmark,
                        'pincode': obj.pincode, 'phone_no': obj.phone}
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

        return JsonResponse({'addresses': myAddresses})


class save_address(APIView):
    def post(self, request):
        response = JsonResponse({'Error': 'True'})
        add_serializer = RegAddresses(data=request.data)
        if add_serializer.is_valid():
            add_serializer.save()
            return JsonResponse(add_serializer.data)
        return JsonResponse(add_serializer.errors)


class get_address(APIView):
    def post(self, request):
        address = (list(Addresses.objects.filter(phone_no=request.POST['phone_no']).values()))
        return JsonResponse(address, safe=False)


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    print(12742 * asin(sqrt(a)))
    return 12742 * asin(sqrt(a))


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


def get_products(request):
    # body=request.body.decode('utf-8')
    # print(json.loads(body)['city'])

    if request.method == "POST":
        mlong = float(request.POST['longitude'])
        mlat = float(request.POST['latitude'])
        mcity = request.POST['city']
        print(mcity)


        vendors = Vendors.objects.filter(city__iexact=mcity).filter(status = 'A')
        print(vendors)
        #vendors = Vendors.objects.filter(city__iexact = mcity)
        #print(vendors)
        selected_vendors = []
        myProducts = []

        for vendor in vendors:
            print(type(mlat))
            if distance(mlat, mlong, vendor.vendor_lat, vendor.vendor_long) <7:
                selected_vendors.append(vendor)

        for vendor in selected_vendors:
            products = Vendor_Products.objects.filter(vendor_phone=vendor)

            for product in products:
                obj = CategorizedProducts.objects.filter(product_id=product.product_id)
                d = {}
                d["under_category"] = obj[0].under_category.categoryName
                d["product_name"] = obj[0].product_name
                d["product_id"] = obj[0].product_id
                d["product_price"] = obj[0].product_price
                d["product_rating"] = obj[0].product_rating
                d["product_descp"] = obj[0].product_descp
                d["product_imagepath"] = obj[0].product_imagepath
                # y = json.loads(d.replace("\"",''))
                # list1=[]
                myProducts.append((d))
            # myProducts.add(list1)
        myProducts = unique(myProducts)
        print(myProducts)
        dict = {"Prod": (myProducts)}

        return JsonResponse(dict, safe=False)

    else:
        return JsonResponse({'error': 'Not a POST request'})


def update_order(orderid, vendors, products, d_boys):
    orders = Orders.objects.filter(order_id=orderid)
    pl = len(products)
    for i in range(vl):
        pll = len(products[i])
        for j in range(vll):
            plll = len(products[i][j])
            for k in pll:
                obj = orders.get(product_id=products[i][j][k])
                obj.update(vendor_phone=vendors[i][j],
                           delivery_boy_phone=Delivery_Boys.objects.get(phone_no=d_boys[i][j]))