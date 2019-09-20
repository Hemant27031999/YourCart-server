from django.db import models

# Create your models here.
class Category(models.Model):
    categoryId = models.IntegerField()
    categoryName = models.CharField(unique=True, max_length=255)
    categoryImagePath = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.categoryName


class CategorizedProducts(models.Model):
    under_category = models.IntegerField()
    product_name = models.CharField(unique=True, max_length=255)
    product_id = models.IntegerField()
    product_price = models.IntegerField()
    product_rating = models.FloatField()
    product_descp = models.CharField(max_length=255)
    product_imagepath = models.CharField(max_length=255, default='media/images/clothing.png')

    def __str__(self):
        return self.product_name


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')
