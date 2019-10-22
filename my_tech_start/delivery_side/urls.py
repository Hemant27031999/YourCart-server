from django.urls import path

from . import views

urlpatterns = [
    path('confirm_order/', views.order_confirm, name='confirmorder'),
    path('vendor_details/', views.vendor_details, name= 'vendor_details'),
    path('cust_details/', views.cust_details, name= 'cust_details'),
    path('del_details/', views.del_boy_details, name= 'del_details'),
]
