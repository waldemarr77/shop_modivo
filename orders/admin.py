from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'address']
    list_filter = ['status',]
    list_display = ['user', 'address', 'status', 'created_at']
    ordering = ['-created_at',]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ['order__user__username', 'variant__product__name']
    list_display = ['order', 'variant', 'price', 'quantity']
    ordering = ['-price',]


