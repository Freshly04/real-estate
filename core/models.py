from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Mate:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def _str_(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name="product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)
    stock = models.IntegerField()
    modified_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images")

    def _str_(self):
        return self.name
