from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'created_at']
    list_filter = ['created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book_id', 'quantity']
    list_filter = ['cart']
