from django import forms
from .models import Product, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields = ('first_name' , 'last_name' , 'address' ,'zipcode' , 'city' ,)

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('category', 'title', 'description', 'price', 'image',)