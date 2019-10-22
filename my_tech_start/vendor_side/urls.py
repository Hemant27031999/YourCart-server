from django.urls import path

from . import views

urlpatterns = [
    path('check/', views.check_vendor, name='check'),
    path('save_products/', views.save_vendor_products, name='saveproducts'),
    path('activate/', views.activate, name='activate'),
    path('history/', views.order_history, name='history'),
]
