from django.db import models
from base_tech.models import *

# Create your models here.


class DeliveryBoyOrders(models.Model):
    del_boy_no = models.ForeignKey(Delivery_Boys, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=500)
    accepted = models.BooleanField()