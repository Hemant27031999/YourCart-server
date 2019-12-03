"""my_tech_start URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from base_tech import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup1/', views.initialsignup, name='signup1'),
    path('place_order/', views.place_order, name='place_order'),
    path('subscribe_order/', views.subscribe_order, name='subscribe_order'),
    path('getaccess/', views.getaccess, name='getaccess'),
    path('login/', views.loginuser, name='loginuser'),
    path('cust_orders/', views.get_order_history, name='orderhistory'),
    path('paytm/', include('paytm.urls')),
    path('image_upload/', views.hotel_image_view, name = 'image_upload'),
    path('success', views.success, name = 'success'),
    path('hotel_images/', views.display_hotel_images, name = 'hotel_images'),
    path('serve/', views.send_file, name = 'serve'),
    path('category/', views.loadAllCategories, name = 'loadAllCategories'),
    path('category/<int:categoryId>/', views.loadSingleCategory, name='loadSingleCategory'),
    path('getProducts/', views.get_products, name='getProducts'),
    path('address/', views.save_address.as_view(),name='save_address'),
    path('get_address/', views.get_address.as_view(),name='save_address'),
    path('chat/', include('base_tech.urls')),
    path('vendor/', include('vendor_side.urls')),
    path('delivery/', include('delivery_side.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
