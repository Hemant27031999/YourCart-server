from django.db import models
from django.utils import timezone
import uuid


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

class indep_Addresses(models.Model):
    house_no = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    landmark = models.CharField(max_length=100)
    pincode = models.IntegerField()

class Orders(models.Model):
    order_id = models.CharField(primary_key=False, editable=True, default=uuid.uuid4, max_length=500)
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    order_date = models.DateField((u"Order date"), auto_now_add=True)
    order_time = models.TimeField((u"Order time"), auto_now_add=True)
    address = models.CharField(max_length=500)
    phone_no = models.ForeignKey(RegUser, to_field='phone_no', on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

class Vendors(models.Model):
    phone_no = models.CharField(primary_key=True, max_length=255)
    vendor_lat = models.FloatField()
    vendor_long = models.FloatField()
    city = models.CharField(unique=False, max_length=255)


class Vendor_Products(models.Model):
    serial = models.AutoField(primary_key=True)
    item_name = models.CharField(unique=False, max_length=255)
    vendor_phone = models.ForeignKey(Vendors,on_delete=models.CASCADE)
