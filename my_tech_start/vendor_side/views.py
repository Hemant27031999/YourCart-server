from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse, HttpResponse, FileResponse

# Create your views here.
def check_vendor(request):
	if request.method == 'POST':
		obj = Vendors.objects.get(vendor_id=request.POST['vendor_id'])
		if obj is not None:
			response = {
				'vendor_phone' : obj.phone_no,
				'vendor_id' : request.POST['vendor_id'],
				'found' : 'true'
			}
		else:
			response = {
				'vendor_phone' : '',
				'vendor_id' : request.POST['vendor_id'],
				'found' : 'false'
			}
		return JsonRsponse(response)
	response = {
		'error' : 'Invalid'
	}
	return JsonRsponse(response)

def send_all_products():
	obj = CategorizedProducts.objects.all()
	all_products = list(obj)
	data = {
		'products' : all_products
	}

def save_vendor_products(request):
	if request.method == 'POST':
		products = request.POST.getlist('products')
		objs = []
		l = len(products)
		for product in products:
			obj = Vendor_Products(product_id = product, vendor_phone = Vendors.objects.get(phone_no=request.POST['vendor_phone']))
			objs.append(obj)
		Vendor_Products.objects.bulk_create(objs, l)

def activate(request):
	if request.method == 'POST':
		obj = Vendors.objects.get(phone_no=request.POST['vendor_phone'])
		if request.POST['status'] == active:
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
