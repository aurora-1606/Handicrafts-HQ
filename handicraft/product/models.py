from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image=models.ImageField(upload_to='uploads/product_images/',blank=True,null=True);
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return self.title

class Order(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    zipcode=models.CharField(max_length=255)
    paid_amount=models.IntegerField(blank=True, null=True)
    is_paid=models.BooleanField(default=False)
    merchant_id=models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null= True)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order  = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items',on_delete=models.CASCADE)
    price=models.IntegerField()
    quantity=models.IntegerField(default=1)

    
