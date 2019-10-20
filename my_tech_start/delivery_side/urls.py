from django.urls import path

from . import views

urlpatterns = [
    path('confirm_order/', views.order_confirm, name='confirmorder'),
]