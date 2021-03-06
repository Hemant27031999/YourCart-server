from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from pusher import Pusher

pusher = Pusher(app_id=u'884349', key=u'7c495f369f4053064877', secret=u'1f0f6089002fcb5d3ce1', cluster=u'ap2', ssl=True)


# Create your views here.
def check_vendor(request):
	if request.method == 'POST':
		try:
			obj = Vendors.objects.get(vendor_id=request.POST['vendor_id'])
			response = {
				'vendor_phone': obj.phone_no,
				'vendor_name': obj.name,
				'vendor_id': request.POST['vendor_id'],
				'found': 'true'
			}
		except:
			response = {
				'vendor_phone': '',
				'vendor_name': '',
				'vendor_id': request.POST['vendor_id'],
				'found': 'false'
			}
		return JsonResponse(response)
	response = {
		'error': 'Invalid'
	}
	return JsonResponse(response)

def send_prev_products(request):
	if request.method == 'POST':
		objs = Vendor_Products.objects.filter(vendor_phone=request.POST['vendor_phone'])
		all_products = list(objs)
		no_prod = len(all_products)
		obj_list = []
		print(all_products)
		for i in range(no_prod):
			print(all_products[i].product_id)
			obj = CategorizedProducts.objects.get(product_id=all_products[i].product_id)
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
			'no_prod': no_prod,
			'products': obj_list
		}
		return JsonResponse(data)
	else:
		return JsonResponse({"error": "invalid!"})


def pusher_authentication(request):
	print(request.headers['vendor-phone'])
	auth = pusher.authenticate(
		channel="private-"+request.headers['vendor-phone'],
		socket_id='1234.1234'
	)
	return JsonResponse(auth)


def send_all_products(request):
	if request.method == 'GET':
		objs = CategorizedProducts.objects.all()
		all_products = list(objs)
		no_prod = len(all_products)
		obj_list = []
		for i in range(no_prod):
			print(all_products[i].product_id)
			get_id = int(all_products[i].product_id)
			obj = CategorizedProducts.objects.get(product_id=get_id)
			print(obj)
			prod = {
				'prod_id': get_id,
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
			'no_prod': no_prod,
			'products': obj_list
		}
		print(data['products'][0]['prod_id'])
		return JsonResponse(data)


def save_vendor_products(request):
	if request.method == 'POST':
		products = request.POST.getlist('products')
		print(Vendors.objects.get(phone_no=request.POST['vendor_phone']))
		old_prods = Vendor_Products.objects.filter(vendor_phone=Vendors.objects.get(phone_no=request.POST['vendor_phone']))
		old_prods.delete()
		objs = []
		l = len(products)
		for product in products:
			obj = Vendor_Products(product_id = product, vendor_phone=Vendors.objects.get(phone_no=request.POST['vendor_phone']))
			objs.append(obj)
		Vendor_Products.objects.bulk_create(objs, l)
		response = {
			'success': 'true'
		}
		return JsonResponse(response)


def activate(request):
	if request.method == 'POST':
		obj = Vendors.objects.get(phone_no=request.POST['vendor_phone'])
		if request.POST['status'] == 'active':
			obj.status='A'
			obj.save()
		else:
			obj.status='I'
			obj.save()
		response = {
			'success': 'true',
			'status': request.POST['status']
		}
		return JsonResponse(response)
	response = {
		'success': 'false',
		'status': ''
	}
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


def order_history(request):
	if request.method == 'POST':
		details = []
		print(request.POST.get('vendor_phone'))
		order_details = list(prev_orders.objects.filter(vendor_phone = request.POST.get('vendor_phone'),order_status = "D"))
		print("order_details",order_details)
		order_ids = []
		for order_detail in order_details:
			order_ids.append(order_detail.order_id)
		order_ids = unique(order_ids)
		print("order_ids",order_ids)
		no_order = len(order_ids)
		myorders = []
		for order_id in order_ids:
			d={}
			d["order_id"] = order_id
			items = []
			products = list(prev_orders.objects.filter(vendor_phone = request.POST['vendor_phone'],order_status = "D",order_id = order_id))
			for product in products:
				obj = CategorizedProducts.objects.filter(product_id=product.product_id)
				print("obj",obj)
				if product.status == "A":
					check = True
				else:
					check = False
				prod = {
					'prod_id': obj[0].product_id,
					'prod_name': obj[0].product_name,
					'category_name': obj[0].under_category.categoryName,
					'category_id': obj[0].under_category.categoryId,
					'prod_price': obj[0].product_price,
					'prod_rating': obj[0].product_rating,
					'prod_desc': obj[0].product_descp,
					'prod_img': obj[0].product_imagepath,
					'check': check
				}
				items.append(prod)
			d["items"] = items
			print(myorders)
			myorders.append(d)


		dict = {
			"no_order" : no_order ,
			"orders" : myorders
		}

		return JsonResponse(dict,safe = False)


def order_ongoing(request):
	if request.method == 'POST':
		details = []
		print(request.POST.get('vendor_phone'))
		order_details = list(prev_orders.objects.filter(vendor_phone = request.POST.get('vendor_phone'),order_status = "A"))
		print("order_details",order_details)
		order_ids = []
		for order_detail in order_details:
			order_ids.append(order_detail.order_id)
		order_ids = unique(order_ids)
		print("order_ids",order_ids)
		no_order = len(order_ids)
		myorders = []
		for order_id in order_ids:
			d={}
			d["order_id"] = order_id
			items = []
			products = list(prev_orders.objects.filter(vendor_phone = request.POST['vendor_phone'],order_status = "A",order_id = order_id))
			for product in products:
				obj = CategorizedProducts.objects.filter(product_id=product.product_id)
				print("obj",obj)
				if product.status == "A":
					check = True
				else:
					check = False
				prod = {
					'prod_id': obj[0].product_id,
					'prod_name': obj[0].product_name,
					'category_name': obj[0].under_category.categoryName,
					'category_id': obj[0].under_category.categoryId,
					'prod_price': obj[0].product_price,
					'prod_rating': obj[0].product_rating,
					'prod_desc': obj[0].product_descp,
					'prod_img': obj[0].product_imagepath,
					'check': check
				}
				items.append(prod)
			d["items"] = items
			print(myorders)
			myorders.append(d)


		dict = {
			"no_order" : no_order ,
			"orders" : myorders
		}

		return JsonResponse(dict,safe = False)


def delivery_details(request):
	if request.method == 'POST':
		objs = Orders.objects.filter(order_id=request.POST['order_id'], vendor_phone=request.POST['vendor_phone'])
		details = list(objs)
		name = ''
		phone = ''
		if not details[0].delivery_boy_phone.name:
			name = 'noName'
			phone = 'noPhone'
		else:
			name = details[0].delivery_boy_phone.name
			phone = details[0].delivery_boy_phone.phone_no

		data = {
			'order_id': request.POST['order_id'],
			'vendor_phone': request.POST['vendor_phone'],
			'del_boy_name': name,
			'del_boy_phone': phone
		}
		return JsonResponse(data)
	return JsonResponse({'error': 'invalid'})


def pusher_check(request):
	#data = {
	#	'products': 'abcd'
	#}
	#pusher.trigger('my-channel', 'my-event', data)
	#return JsonResponse(data)
	send_vendor_order('098', '0987', '09876')
	return JsonResponse({'abc':'abc'})


def send_vendor_order(order_id,vendor_phone, items, quantities):
	l = len(items)
	order_items = []
	for i in range(l):
		obj = CategorizedProducts.objects.get(product_id=items[i])
		d = {
			'category_name': obj.under_category.categoryName,
			'prod_name': obj.product_name,
			'prod_id': obj.product_id,
			'prod_price': obj.product_price,
			'prod_rating': obj.product_rating,
			'prod_desc': obj.product_descp,
			'prod_img': obj.product_imagepath,
			'quantity': quantities[i],
			'check': False,
		}
		order_items.append(d)
	data={
		'order_id':str(order_id),
	#	'vendor_phone': vendor_phone,
	#	'no_prod': l,
		'items': order_items
	}
	#vendor = 'vendor'
	print(type(vendor_phone))
	#phone = str(vendor_phone)
	channel_name = 'vendor'+vendor_phone
	print(data)
	print(channel_name)
	pusher.trigger(channel_name, 'my-event', data)


def order_prepared(request):
	if request.method == 'POST':
		data = {
			'order_id': request.POST['order_id'],
			'status': 'prepared'
		}
		print(data)
		pusher.trigger('my-channel', 'my-event', data)
		response = {'success': 'true'}
		return JsonResponse(response)
	response = {'success': 'true'}
	return JsonResponse(response)

def order_dispatched(request):
	if request.method == 'POST':
		order_id = request.POST['order_id']
		vendor_phone = request.POST['vendor_phone']
		obj = prev_orders.objects.filter(order_id = order_id,vendor_phone = vendor_phone)
        # if obj[0].order_status == "A":

		if obj[0].order_status == "A":
			vendor = Vendors.objects.get(phone_no = vendor_phone)
			print(vendor)
			vendor.current_no_orders = vendor.current_no_orders - 1
			print(vendor.current_no_orders)
			vendor.save()
			prev_orders.objects.filter(order_id = order_id,vendor_phone = vendor_phone).update(order_status = "D")

		response = {'success': 'true'}
		return JsonResponse(response)

		# response = {'success': 'true'}
        # return JsonResponse(response)
