from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse

# Create your views here.


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