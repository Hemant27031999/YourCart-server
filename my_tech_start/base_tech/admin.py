from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Orders)
admin.site.register(RegUser)
admin.site.register(Category)
admin.site.register(CategorizedProducts)
admin.site.register(Addresses)
admin.site.register(indep_Addresses)
admin.site.register(Vendors)
admin.site.register(Vendor_Products)
admin.site.register(Cells)
admin.site.register(Serving_Vendors)
admin.site.register(Delivery_Boys)
admin.site.register(Deliverying_Boys)
admin.site.register(Subscribed_Orders)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'customer_phone', 'order_time')
