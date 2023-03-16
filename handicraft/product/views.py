from django.shortcuts import render
from .models import Product
def product_detail(request,slug):

    product = Product.objects.get(slug=slug)

    return render(request, 'product/product_detail.html', {
        'product': product
    })
