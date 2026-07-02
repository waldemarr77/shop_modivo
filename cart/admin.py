from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['user__username',]
    list_display = ['user', 'created_at']
    ordering = ['-created_at',]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['cart__user__username', 'variant__product__name']
    list_filter = ['variant__size',]
    list_display = ['cart', 'variant', 'quantity']
    ordering = ['-quantity',]