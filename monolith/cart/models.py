from django.db import models
from accounts.models import Customer
from books.models import Book


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart {self.id} - {self.customer.email}"


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book']

    def __str__(self):
        return f"{self.book.title} x{self.quantity}"
