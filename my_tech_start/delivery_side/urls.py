from django.urls import path

from . import views

urlpatterns = [

    path('confirm_order/', views.order_confirm, name='confirmorder'),
    path('vendor_details/', views.vendor_details, name= 'vendor_details'),
    path('cust_details/', views.cust_details, name= 'cust_details'),
    path('del_details/', views.del_boy_details, name= 'del_details'),
    path('confirm_order/', views.order_confirm, name='confirm_order'),
    path('reached_vendor/', views.reached_vendor, name='reached_vendor'),
    path('pickedup/', views.order_pickedup, name='pickedup'),
    path('reached_customer/', views.reached_customer, name='reached_customer'),
    path('delivered/', views.order_delivered, name='delivered'),
    path('check/', views.check_delivery_boy, name='check'),
]
