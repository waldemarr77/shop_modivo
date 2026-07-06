from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'product__name']
    list_filter = ['rating',]
    list_display = ['user', 'product', 'rating', 'created_at']
    ordering = ['-created_at',]