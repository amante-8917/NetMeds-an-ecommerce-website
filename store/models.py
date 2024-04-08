from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Seller(AbstractUser):
    models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, default="")
    product_description = models.TextField(max_length=500, default="")
    product_category = models.CharField(max_length=50, default="")
    product_price = models.CharField(max_length=50, default="")
    product_publishing_date = models.DateTimeField(default=datetime)
    product_status = models.CharField(max_length=50, default="")
    product_year = models.CharField(max_length=2, default="")
    product_image = models.ImageField(upload_to="images", default="")
    product_listed_by = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.product_name


class Query(models.Model):
    query_id = models.AutoField(primary_key=True)
    query_owner_name = models.CharField(max_length=50, default="")
    query_owner_email = models.EmailField(max_length=50, default="")
    query_owner_phone = models.CharField(max_length=13, default="")
    query_description = models.TextField(max_length=500)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    product_owner_id = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
