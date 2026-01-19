"""
Django views - Framework layer (API endpoints)
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from infrastructure.repositories import (
    CustomerRepository, BookRepository,
    CartRepository, CartItemRepository
)
from usecases.customer_usecases import RegisterCustomerUseCase, LoginCustomerUseCase
from usecases.book_usecases import GetBookCatalogUseCase, GetBookByIdUseCase
from usecases.cart_usecases import AddToCartUseCase, ViewCartUseCase
from interfaces.serializers import (
    CustomerSerializer, BookSerializer,
    CartSerializer, CartItemSerializer
)


# Initialize repositories
customer_repo = CustomerRepository()
book_repo = BookRepository()
cart_repo = CartRepository()
cart_item_repo = CartItemRepository()


@api_view(['POST'])
def register(request):
    """Customer registration"""
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not all([name, email, password]):
            return Response(
                {'error': 'Missing required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        use_case = RegisterCustomerUseCase(customer_repo)
        customer = use_case.execute(name, email, password)
        
        return Response(
            CustomerSerializer.to_dict(customer),
            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def login(request):
    """Customer login"""
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not all([email, password]):
            return Response(
                {'error': 'Missing email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        use_case = LoginCustomerUseCase(customer_repo)
        customer = use_case.execute(email, password)
        
        if customer:
            return Response(
                CustomerSerializer.to_dict(customer),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def book_list(request):
    """View book catalog"""
    try:
        use_case = GetBookCatalogUseCase(book_repo)
        books = use_case.execute()
        return Response(
            BookSerializer.to_dict_list(books),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def book_detail(request, book_id):
    """Get book details"""
    try:
        use_case = GetBookByIdUseCase(book_repo)
        book = use_case.execute(book_id)
        
        if book:
            return Response(
                BookSerializer.to_dict(book),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def add_to_cart(request, customer_id):
    """Add books to the shopping cart"""
    try:
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        if not book_id:
            return Response(
                {'error': 'Missing book_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        use_case = AddToCartUseCase(
            cart_repo, cart_item_repo,
            customer_repo, book_repo
        )
        cart = use_case.execute(customer_id, book_id, quantity)
        
        # Get cart items with books
        items = cart_item_repo.get_by_cart_id(cart.id)
        books = [book_repo.get_by_id(item.book_id) for item in items]
        
        return Response(
            CartSerializer.to_dict(cart, items, books),
            status=status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def view_cart(request, customer_id):
    """View shopping cart contents"""
    try:
        use_case = ViewCartUseCase(cart_repo, cart_item_repo, customer_repo)
        cart, items = use_case.execute(customer_id)
        
        if cart is None:
            return Response(
                {'message': 'Cart is empty', 'items': []},
                status=status.HTTP_200_OK
            )
        
        # Get books for items
        books = [book_repo.get_by_id(item.book_id) for item in items]
        
        return Response(
            CartSerializer.to_dict(cart, items, books),
            status=status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
