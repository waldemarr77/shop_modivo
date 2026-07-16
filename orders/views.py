from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.product.price
                )
                item.variant.stock -= item.quantity
                item.variant.save()

            cart_items.delete()
            cache.delete(f'cart_{request.user.id}')

        send_order_confirmation.delay(order.id, request.user.email)

        return Response(
            {
                'message': 'Замовлення успішно оформлено!',
                'order_id': order.id,
                'status': order.status
            },
            status=status.HTTP_201_CREATED
        )
