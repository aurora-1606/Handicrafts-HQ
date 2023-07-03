from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm

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

@login_required
def checkout(request):
    cart=Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price=0
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by=request.user
            order.paid_amount= total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = item['quantity']
                price = product.price * quantity

                item = OrderItem.objects.create(order=order,product=product,price=price,quantity=quantity)
            cart.clear()
            return redirect('myaccount')
    else:
        form= OrderForm()
    return render(request, 'product/checkout.html' , { 'cart' : cart , 'form' : form,})

def product_detail(request,slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'product/product_detail.html', {
        'product': product
    })
