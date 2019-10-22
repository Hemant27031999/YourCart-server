from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse
from pusher import Pusher

pusher = Pusher(app_id=u'884349', key=u'7c495f369f4053064877', secret=u'1f0f6089002fcb5d3ce1', cluster=u'ap2', ssl=True)

# Create your views here.


def check_delivery_boy(request):
    if request.method == 'POST':
        try:
            obj = Delivery_Boys.objects.get(del_boy_id=request.POST['del_boy_id'])
            response = {
                'del_boy_phone': obj.phone_no,
                'del_boy_id': request.POST['del_boy_id'],
                'found': 'true'
            }
        except:
            response = {
                'del_boy_phone': '',
                'del_boy_id': request.POST['del_boy_id'],
                'found': 'false'
            }
        return JsonResponse(response)
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def order_confirm(request):
    if request.method == 'POST':
        if request.POST['accepted'] == 'true':
            DeliveryBoyOrders.create(
                del_boy_no=Delivery_Boys.objects.get(phone_no=request.POST['del_boy_no']),
                order_id=request.POST['order_id'],
                accepted=True
            )
        else:
            DeliveryBoyOrders.create(
                del_boy_no=Delivery_Boys.objects.get(phone_no=request.POST['del_boy_no']),
                order_id=request.POST['order_id'],
                accepted=False
            )
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'false'}
    return JsonResponse(response)


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

def vendor_details(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        del_phone = request.POST['phone_no']
        myorder = Orders.objects.filter(order_id = order_id,delivery_boy_phone = del_phone)
        # vendor_phones =(myorder.vendor_phone)
        print("myorder",myorder)
        vendor_phones = []
        for order in myorder:
            vendor_phones.append(order.vendor_phone)
        print("vendor_phones",vendor_phones)
        vendor_phones = unique(vendor_phones)
        print("vendor_phones_unique",vendor_phones)
        details = []
        for vendor_phone in vendor_phones:
            d={}

            ven_order = myorder.filter(vendor_phone = vendor_phone)
            print("ven_order",ven_order)
            products = []
            for product in ven_order:
                products.append(product.product_name)
            print("products",products)
            d["vendor_phone"] = vendor_phone
            d["products"] = products
            print("d",d)
            details.append(d)
        dict= {"details":details}
        return JsonResponse(dict, safe=False)

def cust_details(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        del_phone = request.POST['phone_no']
        myorder = Orders.objects.filter(order_id = order_id,delivery_boy_phone = del_phone)
        address = myorder[0].address
        cust_lat = myorder[0].cust_lat
        cust_long = myorder[0].cust_long
        phone_no = myorder[0].customer_phone
        data = {
            "customer_phone": phone_no.phone_no,
            "cust_lat":cust_lat,
            "cust_long":cust_long,
            "address":address
        }
        print(data)
        return JsonResponse(data,safe = False)

def del_boy_details(request):
    if request.method == 'POST':
        isprimary = request.POST['isprimary']
        del_phone = request.POST['phone_no']
        order_id = request.POST['order_id']
        #filter wrt order_id
        myorder = Orders.objects.filter(order_id = order_id)
        print("myorder",myorder)
        if isprimary == "True":
            del_boy_list = []
            for boy in myorder:
                del_boy_list.append(boy.delivery_boy_phone.phone_no)
            print(del_boy_list )
            del_boy_list = unique(del_boy_list)
            del_boy_list.remove(del_phone)
            dict = {"delivery_boys":del_boy_list}
            return JsonResponse(dict,safe = False)

        else:
            primaryBoy = myorder.filter(delboy_type = "P")[0]
            print(primaryBoy)
            dict = {"primary_boy": primaryBoy.delivery_boy_phone.phone_no}
            return JsonResponse(dict,safe = False)

def order_delivered(request):
    if request.method == 'POST':
        if request.POST['delivered'] == 'true':
            data = {
                'order_id': request.POST['order_id'],
                'status': 'delivered'
            }
            pusher.trigger('my-channel', 'my-event', data)
            response = {'success': 'true'}
            return JsonResponse(response)
        else:
            data = {
                'order_id': request.POST['order_id'],
                'status': 'could not be delivered'
            }
            pusher.trigger('my-channel', 'my-event', data)
            response = {'success': 'true'}
            return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def reached_vendor(request):
    if request.method == 'POST':
        data = {
            'order_id': request.POST['order_id'],
            'status': 'reached vendor'
        }
        pusher.trigger('my-channel', 'my-event', data)
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def order_pickedup(request):
    if request.method == 'POST':
        data = {
            'order_id': request.POST['order_id'],
            'status': 'pickedup'
        }
        pusher.trigger('my-channel', 'my-event', data)
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def reached_customer(request):
    if request.method == 'POST':
        data = {
            'order_id': request.POST['order_id'],
            'status': 'reached customer'
        }
        pusher.trigger('my-channel', 'my-event', data)
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)
