from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'variant', 'quantity', 'price']
        read_only_fields = ['id', 'order', 'price']