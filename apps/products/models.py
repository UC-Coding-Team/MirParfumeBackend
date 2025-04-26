from django.db import models
from apps.common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categories/")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
