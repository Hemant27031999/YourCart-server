from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse, HttpResponse, FileResponse
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
			print(all_products[i].product_id.product_id)
			obj = CategorizedProducts.objects.get(product_id=all_products[i].product_id.product_id)
			prod = {
				'prod_id': obj.product_id,
				'prod_name': obj.product_name,
				'category_name': obj.under_category.categoryName,
				'category_id': obj.under_category.categoryId,
				'prod_price': obj.product_price,
				'prod_rating': obj.product_rating,
				'prod_desc': obj.product_descp,
				'prod_img': obj.product_imagepath,
				'check': True
			}
			obj_list.append(prod)
		data = {
			'no_prod': no_prod,
			'vendor_phone': request.POST['vendor_phone'],
			'products': obj_list
		}
		return JsonResponse(data)




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
			obj = Vendor_Products(product_id = CategorizedProducts.objects.get(product_id=product), vendor_phone=Vendors.objects.get(phone_no=request.POST['vendor_phone']))
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
			'vendor_phone' : request.POST['vendor_phone'],
			'success' : 'true'
		}
		return JsonResponse(response)
	response = {
		'error' : 'Invalid'
	}
	return JsonResponse(response)


def order_history(request):
	if request.method == 'POST':
		details = []
		order_details = list(prev_orders.objects.filter(order_id = request.POST['order_id'], vendor_phone = request.POST['vendor_phone']))
		for order_detail in order_details:
			d={}
			d["product_name"] = order_detail.product_name
			d["status"] = order_detail.status
			details.append(d)

		dict = {"detail" : details }

		return JsonResponse(dict,safe = False)


def pusher_check(request):
	#data = {
	#	'products': 'abcd'
	#}
	#pusher.trigger('my-channel', 'my-event', data)
	#return JsonResponse(data)
	send_order('098')


def send_order(order_id, items, quantities, ):
	data = {
		'vendor_phone': '987654',
		'order_id': order_id,
		'items': items,
		'quantities': quantities
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
