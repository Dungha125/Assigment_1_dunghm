from rest_framework import serializers
from .models import Cart, CartItem
from books.serializers import BookSerializer


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'created_at', 'items']
        read_only_fields = ['created_at']


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
