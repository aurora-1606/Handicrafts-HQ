import json
import stripe

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm
from django.conf import settings

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')

def success(request):
    return render(request,'product/success.html')

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

    if cart.get_total_cost() == 0:
        return redirect('cart_view')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price=0
        items = []
        for item in cart:
            product = item['product']
            total_price += product.price * int(item['quantity'])

            items.append({
                'price_data' : {
                    'currency' :'inr',
                    'product_data' : {
                        'name' :product.title,
                    },
                    'unit_amount': product.price*100,
                },
                'quantity' : item['quantity']

            })

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.01:8000/cart/success',
        cancel_url='http://127.0.01:8000/cart/'
        )

        payment_intent=session.payment_intent

        order= Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            zipcode=data['zipcode'],
            city=data['city'],
            created_by=request.user,
            is_paid= True,
            payment_intent = payment_intent,
            paid_amount= total_price,
        )

        for item in cart:
            product = item['product']
            quantity = item['quantity']
            price = product.price * quantity

            item = OrderItem.objects.create(order=order,product=product,price=price,quantity=quantity)
        cart.clear()
        print(session)
        print(payment_intent)
        return JsonResponse({'session' : session, 'order': payment_intent})
    else:
        form= OrderForm()
    return render(request, 'product/checkout.html' , { 'cart' : cart , 'form' : form, 'pub_key' : settings.STRIPE_PUB_KEY,})

def product_detail(request,slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'product/product_detail.html', {
        'product': product
    })
