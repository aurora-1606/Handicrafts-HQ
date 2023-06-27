from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product
from .cart import Cart

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')
def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1

        if action == 'decrease':
            quantity= -1
        cart=Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart_view')



def remove_from_cart(request, product_id):
    cart=Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')
    

def cart_view(request):
    cart=Cart(request)

    return render(request, 'product/cart_view.html', { 'cart' : cart})

def product_detail(request,slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'product/product_detail.html', {
        'product': product
    })
