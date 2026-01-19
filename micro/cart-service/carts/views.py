from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer
from .services import CustomerService, BookService


@api_view(['POST'])
def add_to_cart(request, customer_id):
    """Add books to the shopping cart"""
    # Validate customer exists via customer-service
    customer_data = CustomerService.get_customer(customer_id)
    if not customer_data:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    book_id = serializer.validated_data['book_id']
    quantity = serializer.validated_data['quantity']

    # Validate book exists and has stock via book-service
    book_data = BookService.get_book(book_id)
    if not book_data:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if book_data['stock'] < quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create cart for customer
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)

    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id,
        defaults={'quantity': quantity}
    )

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    # Fetch cart items with book data
    items = CartItem.objects.filter(cart=cart)
    book_ids = [item.book_id for item in items]
    books_data = BookService.get_books_by_ids(book_ids)
    books_dict = {book['id']: book for book in books_data}

    # Attach book data to items
    for item in items:
        item._book_data = books_dict.get(item.book_id)

    cart._customer_data = customer_data

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_cart(request, customer_id):
    """View shopping cart contents"""
    # Validate customer exists via customer-service
    customer_data = CustomerService.get_customer(customer_id)
    if not customer_data:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart.objects.get(customer_id=customer_id)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart is empty', 'items': []}, status=status.HTTP_200_OK)

    # Fetch cart items with book data
    items = CartItem.objects.filter(cart=cart)
    book_ids = [item.book_id for item in items]
    books_data = BookService.get_books_by_ids(book_ids)
    books_dict = {book['id']: book for book in books_data}

    # Attach book data to items
    for item in items:
        item._book_data = books_dict.get(item.book_id)

    cart._customer_data = customer_data

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)
