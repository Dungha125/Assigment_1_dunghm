"""
Django ORM models - Framework layer
"""
from django.db import models


class CustomerModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.email


class BookModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class CartModel(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart {self.id} - Customer {self.customer_id}"


class CartItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    cart_id = models.IntegerField()
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart_id', 'book_id']

    def __str__(self):
        return f"CartItem {self.id} - Book {self.book_id} x{self.quantity}"
