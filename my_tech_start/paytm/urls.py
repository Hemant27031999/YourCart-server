from django.conf.urls import include, url
from paytm import views
from django.urls import path

urlpatterns = [
    # Examples:
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    path('response/', views.response, name='response'),
]
