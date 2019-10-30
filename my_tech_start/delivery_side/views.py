from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse
from pusher import Pusher
from vendor_side.models import *

pusher = Pusher(app_id=u'884349', key=u'7c495f369f4053064877', secret=u'1f0f6089002fcb5d3ce1', cluster=u'ap2', ssl=True)

# Create your views here.


def check_delivery_boy(request):
    if request.method == 'POST':
        try:
            obj = Delivery_Boys.objects.get(del_boy_id=request.POST['del_boy_id'])
            response = {
                'del_boy_phone': obj.phone_no,
                'del_boy_name': obj.name,
                'del_boy_id': request.POST['del_boy_id'],
                'found': 'true'
            }
        except:
            response = {
                'del_boy_phone': '',
                'del_boy_name': '',
                'del_boy_id': request.POST['del_boy_id'],
                'found': 'false'
            }
        return JsonResponse(response)
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def activate_delboy(request):
    if request.method == 'POST':
        obj = Delivery_Boys.objects.get(phone_no=request.POST['delboy_phone'])
        if request.POST['status'] == 'active':
            obj.status='A'
            obj.save()
        else:
            obj.status='I'
            obj.save()
        response = {
            'delboy_phone': request.POST['delboy_phone'],
            'success': 'true'
        }
        return JsonResponse(response)
    response = {
        'delboy_phone': request.POST['delboy_phone'],
        'success': 'false'
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

def send_delivery_order(data,phone_no):
    print(data)
    delivery = 'delivery'
    channel_name = delivery.join(str(phone_no))
    pusher.trigger(channel_name , 'my-event', data)

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
            products_name = []
            for product in ven_order:
                products.append(product.product_id.product_id)
                obj = CategorizedProducts.objects.filter(product_id = product.product_id.product_id)
                products_name.append(obj[0].product_name)
            ven_obj = Vendors.objects.filter(phone_no = vendor_phone)
            print("products",products)
            d["vendor_name"] = ven_obj[0].name
            d["vendor_address"] = ven_obj[0].address
            d["vendor_lat"] = ven_obj[0].vendor_lat
            d["vendor_long"] = ven_obj[0].vendor_long
            d["vendor_phone"] = vendor_phone
            d["products_id"] = products
            d["products_name"] = products_name
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
        del_boy = Delivery_Boys.objects.get(phone_no = del_phone)
        myorder = Orders.objects.filter(order_id = order_id)
        print("myorder",myorder)
        if isprimary == "True":
            del_boy_list = []
            del_name_list = []
            for boy in myorder:
                del_boy_list.append(boy.delivery_boy_phone.phone_no)
                del_name_list.append(boy.delivery_boy_phone.name)


            print(del_boy_list)
            del_boy_list = unique(del_boy_list)
            del_boy_list.remove(del_phone)
            del_name_list.remove(del_boy.name)

            dict = {
                "delivery_boy_phone":del_boy_list,
                "delivery_boy_names":del_name_list
            }
            return JsonResponse(dict,safe = False)

        else:
            primaryBoy = myorder.filter(delboy_type = "P")[0]
            print(primaryBoy)
            dict = {
                "primary_boy": primaryBoy.delivery_boy_phone.phone_no,
                "primary_name": primaryBoy.delivery_boy_phone.name
            }
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


def reached_checkpoint(request):
    if request.method == 'POST':
        data = {
            'order_id': request.POST['order_id'],
            'status': 'reached checkpoint'
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
        # order_id = request.POST['order_id']
        # obj = prev_orders.objects.filter(order_id = order_id)
        # if obj[0].order_status == "A":
        #     vendor_list = Orders.objects.filter(order_id =order_id).values('vendor_phone')
        #     print(vendor_list)
        #     vendor_list = unique(vendor_list)
        #     for vendor in vendor_list:
        #         ven  = Vendors.objects.get(phone_no = vendor['vendor_phone'])
        #         print(ven)
        #         ven.current_no_orders = ven.current_no_orders - 1
        #         print(ven.current_no_orders)
        #         ven.save()
        #     prev_orders.objects.filter(order_id = order_id).update(order_status = "D")

        # for product in products:
        #     product.order_status

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

# def order_picked(request):
#     if request.method == 'POST':
#         order_id = request.POST['order_id']
#         products
