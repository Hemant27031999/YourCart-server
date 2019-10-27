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
				'vendor_id': request.POST['vendor_id'],
				'found': 'true'
			}
		except:
			response = {
				'vendor_phone': '',
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


#def pusher_auth(request):
#	if not request.user.is_authenticated:
#		return HttpResponseForbidden()
#
#	if not request.user.is_member_of_team('designers'):
#		return HttpResponseForbidden()
#
#	pusher_client = Pusher(APP_ID, API_KEY, SECRET_KEY, CLUSTER)
#
#	# We must generate the token with pusher's service
#	payload = pusher_client.authenticate(
#		channel=request.POST['channel_name'],
#		socket_id=request.POST['socket_id'])
#
#	return JsonResponse(payload)


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
			obj.update(status='A')
		else:
			obj.update(status='I')
		response = {
			'vendor_phone': request.POST['vendor_phone'],
			'success': 'true'
		}
		return JsonResponse(response)
	response = {
		'error' : 'Invalid'
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


def pusher_check(request):
	#data = {
	#	'products': 'abcd'
	#}
	#pusher.trigger('my-channel', 'my-event', data)
	#return JsonResponse(data)
	send_vendor_order('098', '0987', '09876')
	return JsonResponse({'abc':'abc'})


def send_vendor_order(vendor_phone, items, quantities):
	l = len(items)
	order_items = []
	for i in range(l):
		obj = CategorizedProducts.objects.get(product_id=items[i])
		d = {
			'under_category': obj.under_category.categoryName,
			'product_name': obj.product_name,
			'product_id': obj.product_id,
			'product_price': obj.product_price,
			'product_rating': obj.product_rating,
			'product_descp': obj.product_descp,
			'product_imagepath': obj.product_imagepath,
			'quantity': quantities[i]
		}
		order_items.append(d)
	data={
		'vendor_phone': vendor_phone,
		'no_prod': l,
		'products': order_items
	}
	print(data)
	pusher.trigger('my-channel', 'my-event', data)


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
