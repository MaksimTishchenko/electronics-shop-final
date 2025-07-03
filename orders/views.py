# orders/views.py
import stripe
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.views import get_cart, cart_clear
from products.models import Product
from django.db import transaction
from django.urls import reverse
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id, user=request.user)

        line_items = [{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.product.name},
                "unit_amount": int(item.price * 100),  # cents
            },
            "quantity": item.quantity,
        } for item in order.items.all()]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse("orders:order_success", kwargs={"order_id": order.id})
            ),
            cancel_url=request.build_absolute_uri("/orders/cancelled/"),
            client_reference_id=order.id
        )

        return redirect(checkout_session.url, code=303)

@login_required
def create_order(request):
    cart = get_cart(request)
    if not cart:
        messages.info(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        address = request.POST.get('delivery_address')
        user = request.user

        try:
            with transaction.atomic():
                total_price = sum(
                    Product.objects.get(id=product_id).price * quantity
                    for product_id, quantity in cart.items()
                )

                order = Order.objects.create(
                    user=user,
                    delivery_address=address,
                    total_price=total_price
                )

                for product_id, quantity in cart.items():
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

            cart_clear(request)
            return redirect('orders:checkout_session', order_id=order.id)

        except Product.DoesNotExist:
            messages.error(request, "Один из товаров не найден")
            return redirect('cart:cart_detail')

    return render(request, 'orders/create.html')


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

