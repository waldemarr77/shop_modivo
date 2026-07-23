import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.core.cache import cache

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .tasks import send_order_confirmation
from cart.models import Cart


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.prefetch_related(
                'cart_item__variant__product'
            ).get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Кошик не знайдено'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = cart.cart_item.all()
        if not cart_items.exists():
            return Response(
                {'error': 'Ваш кошик порожній'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            for item in cart_items:
                if item.variant.stock < item.quantity:
                    return Response(
                        {
                            'error': f'Товару "{item.variant.product.name}" '
                                     f'залишилось лише {item.variant.stock} шт., '
                                     f'а у вас в кошику {item.quantity} шт.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            order = Order.objects.create(
                user=request.user,
                status='pending',
                address=request.data.get('address', '')
            )

            stripe_line_items = []

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.product.price
                )
                item.variant.stock -= item.quantity
                item.variant.save()

                stripe_line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.variant.product.name,
                        },
                        'unit_amount': int(item.variant.product.price * 100),
                    },
                    'quantity': item.quantity,
                })

            cart_items.delete()
            cache.delete(f'cart_{request.user.id}')
            
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=stripe_line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/api/orders/order/') + '?success=true',
                cancel_url=request.build_absolute_uri('/api/orders/order/') + '?canceled=true',
                client_reference_id=str(order.id) 
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        send_order_confirmation.delay(order.id, request.user.email)

        return Response(
            {
                'message': 'Замовлення успішно оформлено!',
                'order_id': order.id,
                'status': order.status,
                'checkout_url': checkout_session.url 
            },
            status=status.HTTP_201_CREATED
        )


class StripeWebhookView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            order_id = session.client_reference_id
            
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = 'paid'
                    order.save()
                    print(f"Замовлення {order_id} успішно оплачено!")
                except Order.DoesNotExist:
                    print(f"Замовлення {order_id} не знайдено в базі!")

        return Response(status=status.HTTP_200_OK)