from django.contrib import admin
from .models import MainCategory, SubCategory, Brand, Product

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name', 'slug']
    ordering = ['-name',]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name', 'slug', 'main_category']
    ordering = ['-name',]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name',]
    ordering = ['-name',]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name', 'brand__name']
    list_filter = ['category__name', 'brand__name']
    list_display = ['category', 'brand', 'name', 'price', 'created_at']
    ordering = ['-created_at',]
    