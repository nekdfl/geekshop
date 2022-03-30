'''models for product and productcategory'''
from email.policy import default
from statistics import quantiles
from unicodedata import category
from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    '''model category'''
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    '''model product'''
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='product_images', blank=True)
    desciption = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantily = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} || {self.category}"
