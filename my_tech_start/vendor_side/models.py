from django.db import models
import uuid
# Create your models here.
class prev_orders(models.Model):
    order_id = models.CharField(primary_key=False, editable=True, default=uuid.uuid4, max_length=500)
    vendor_phone = models.CharField(max_length=500, blank=True, null=True)
    product_name = models.CharField(primary_key=False, editable=True,  max_length=256)
    STATUS = [
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS,default='A')
    ORDER_STATUS = (
        ('D', 'Delivered'),
        ('A', 'Active')
    )
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='A')
