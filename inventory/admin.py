from django.contrib import admin
from .models import Size, ProductVariant

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name',]
    ordering = ['-name',]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'size__name']
    list_filter = ['product__name', 'size__name']
    list_display = ['product', 'size', 'stock', 'sku']
    ordering = ['stock',]