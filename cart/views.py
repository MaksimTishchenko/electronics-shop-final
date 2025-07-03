from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from rest_framework import generics
from .models import CartItem
from .serializers import CartItemSerializer

class CartAddView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_detail(request):
    cart = get_cart(request)
    product_ids = cart.keys()

    if not product_ids:
        return render(request, 'cart/detail.html', {
            'cart_products': [],
            'total_price': 0
        })

    products = Product.objects.filter(id__in=product_ids)

    cart_products = []
    total_price = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        total = product.price * quantity
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })
        total_price += total

    return render(request, 'cart/detail.html', {
        'cart_products': cart_products,
        'total_price': total_price
    })

def cart_add(request, product_id):
    cart = get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(request, cart)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        save_cart(request, cart)
    return redirect('cart:cart_detail')

def cart_clear(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart:cart_detail')