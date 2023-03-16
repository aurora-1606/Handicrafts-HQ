from django.shortcuts import render
from product.models import Product
# Create your views here.
def frontpage(request):
    products = Product.objects.all()[0:5]

    return render(request, 'core/frontpage.html', {
        'products': products
    })
def about(request):
    return render(request,'core/about.html')
