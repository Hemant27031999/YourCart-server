from django.urls import path

from . import views

urlpatterns = [
    path('check/', views.check_vendor, name='check'),
    path('save_products/', views.save_vendor_products, name='saveproducts'),
    path('activate/', views.activate, name='activate'),
    path('send/', views.pusher_check),
    path('get_products/', views.send_all_products, name='getproducts'),
    path('prepared/', views.order_prepared, name='prepared'),
]