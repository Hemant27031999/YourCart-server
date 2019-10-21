from django.db import models
from django.utils import timezone
import uuid
import json

# Create your models here.
class RegUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(primary_key=True, max_length=15)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

class Category(models.Model):
    categoryId = models.IntegerField(primary_key=True)
    categoryName = models.CharField(unique=True, max_length=255)
    categoryImagePath = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.categoryName


class CategorizedProducts(models.Model):
    under_category = models.ForeignKey(Category, on_delete=models.PROTECT)
    product_name = models.CharField(unique=True, max_length=255)
    product_id = models.IntegerField(primary_key=True)
    product_price = models.IntegerField()
    product_rating = models.FloatField()
    product_descp = models.CharField(max_length=255)
    product_imagepath = models.CharField(max_length=255, default='media/images/clothing.png')
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    #vendors = models.ManyToManyField(Vendors)

    def __str__(self):
        return self.product_name


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')


class Addresses(models.Model):
    address_id = models.IntegerField(primary_key=True)
    house_no = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    landmark = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_no = models.ForeignKey(RegUser, to_field='phone_no', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class indep_Addresses(models.Model):
    house_no = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    landmark = models.CharField(max_length=100)
    pincode = models.IntegerField()


class Cells(models.Model):
    Cell_id = models.IntegerField(primary_key=True)
    Cell_lat = models.FloatField()
    Cell_long = models.FloatField()
    no_vendor = models.IntegerField()
    city = models.CharField(unique=False, max_length=255, default = "Roorkee")

class Vendors(models.Model):
    phone_no = models.CharField(primary_key=True, max_length=255)
    vendor_lat = models.FloatField()
    vendor_long = models.FloatField()
    city = models.CharField(unique=False, max_length=255)
    cell = models.ForeignKey(Cells, on_delete =models.CASCADE)
    STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='I',
    )
    total_no_orders = models.IntegerField(default=0)
    current_no_orders = models.IntegerField(default=0)
    busy = models.CharField(max_length=20, blank=True, null=True)

class Serving_Vendors(models.Model):
    phone_no = models.ForeignKey(Vendors, to_field="phone_no", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=500)


class Vendor_Products(models.Model):
    serial = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    vendor_phone = models.ForeignKey(Vendors, on_delete=models.CASCADE)



class Delivery_Boys(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255, primary_key=True)
    address = models.CharField(max_length=500)
    STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='I',
    )
    total_no_orders = models.IntegerField()
    current_no_orders = models.IntegerField()
    busy = models.BooleanField(default = False)
    city = models.CharField(unique=False, max_length=255)
    #delete later
    lat = models.FloatField(default = 28.33)
    long = models.FloatField(default = 77.88)

class Deliverying_Boys(models.Model):
    phone_no = models.ForeignKey(Delivery_Boys, to_field='phone_no', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=500)
    vendor_phone = models.ForeignKey(Vendors, on_delete=models.PROTECT)

class Subscribed_Orders(models.Model):
    sorder_id = models.CharField(primary_key=False, editable=True, default=uuid.uuid4, max_length=100)
    customer_phone = models.ForeignKey(RegUser, on_delete=models.CASCADE)
    delivery_time = models.TimeField((u"Delivery time"))
    start_date = models.DateField((u"Start date"))
    end_date = models.DateField((u"End date"))
    vendor_phone = models.ForeignKey(Vendors, on_delete=models.PROTECT, blank=True, null=True)
    product_id = models.ForeignKey(CategorizedProducts, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    STATUS = [
        ('A', 'Active'),
        ('E', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS,default='A')
    cust_lat = models.CharField(max_length=50, blank=True, null=True)
    cust_long = models.CharField(max_length=50, blank=True, null=True)

class Orders(models.Model):
    order_id = models.CharField(primary_key=False, editable=True, default=uuid.uuid4, max_length=500)
    product_id = models.ForeignKey(CategorizedProducts, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    order_date = models.DateField((u"Order date"), auto_now_add=True)
    order_time = models.TimeField((u"Order time"), auto_now_add=True)
    address = models.CharField(max_length=500)
    customer_phone = models.ForeignKey(RegUser, to_field='phone_no', on_delete=models.CASCADE)
    vendor_phone = models.CharField(max_length=500, blank=True, null=True)
    delivery_boy_phone = models.ForeignKey(Delivery_Boys, on_delete=models.PROTECT, null=True, blank=True)
    ORDER_STATUS = (
        ('D', 'Delivered'),
        ('A', 'Active')
    )
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='A')
    cust_lat = models.CharField(max_length=50, blank=True, null=True)
    cust_long = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.order_id
