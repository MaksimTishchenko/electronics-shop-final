# orders/urls.py

from django.urls import path
from . import views
from .views import CreateCheckoutSessionView
from django.views.generic import TemplateView
app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('checkout-session/<int:order_id>/', CreateCheckoutSessionView.as_view(), name='checkout_session'),
    path('success/', TemplateView.as_view(template_name="orders/success.html"), name='success'),
    path("cancel/", TemplateView.as_view(template_name="orders/cancel.html"), name="cancel"),
]