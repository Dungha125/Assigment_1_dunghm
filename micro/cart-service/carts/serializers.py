from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity']

    def get_book(self, obj):
        # Book data will be fetched from book-service
        return getattr(obj, '_book_data', None)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'customer', 'created_at', 'items']
        read_only_fields = ['created_at']

    def get_customer(self, obj):
        # Customer data will be fetched from customer-service
        return getattr(obj, '_customer_data', None)


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
