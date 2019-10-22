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
            'status': 'picked up'
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