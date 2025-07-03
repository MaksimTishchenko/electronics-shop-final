import json
import stripe
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # Обработка событий
        if event.type == "checkout.session.completed":
            session = event.data.object
            order_id = session.client_reference_id

            try:
                order = Order.objects.get(id=order_id)
                order.status = "paid"
                order.save()
                print(f"✅ Заказ #{order.id} помечен как 'paid'")
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)

        return JsonResponse({'status': 'success'})