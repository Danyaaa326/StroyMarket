from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    characteristics = models.TextField(blank=True, verbose_name='Характеристики')
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_analogs(self):
        price_val = float(self.price)
        return Product.objects.filter(
            category=self.category,
            price__range=(price_val * 0.7, price_val * 1.3)
        ).exclude(id=self.id)

from django.core.files.storage import FileSystemStorage
import os