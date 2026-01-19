from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer
from accounts.models import Customer
from books.models import Book


@api_view(['POST'])
def add_to_cart(request, customer_id):
    """Add books to the shopping cart"""
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    book_id = serializer.validated_data['book_id']
    quantity = serializer.validated_data['quantity']

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if book.stock < quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create cart for customer
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    cart_serializer = CartSerializer(cart)
    return Response(cart_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_cart(request, customer_id):
    """View shopping cart contents"""
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart.objects.get(customer=customer)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart is empty', 'items': []}, status=status.HTTP_200_OK)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)
