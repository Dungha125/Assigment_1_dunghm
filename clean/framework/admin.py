from django.contrib import admin
from .models import CustomerModel, BookModel, CartModel, CartItemModel


@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    search_fields = ['name', 'email']


@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock']
    search_fields = ['title', 'author']


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'created_at']


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id', 'book_id', 'quantity']
