"""
Cart use cases
"""
from typing import List, Tuple, Optional
from domain.entities import Cart, CartItem
from domain.repositories import (
    ICartRepository, ICartItemRepository, 
    ICustomerRepository, IBookRepository
)


class AddToCartUseCase:
    """Add book to cart"""
    
    def __init__(
        self,
        cart_repository: ICartRepository,
        cart_item_repository: ICartItemRepository,
        customer_repository: ICustomerRepository,
        book_repository: IBookRepository
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.customer_repository = customer_repository
        self.book_repository = book_repository
    
    def execute(self, customer_id: int, book_id: int, quantity: int) -> Cart:
        # Validate customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Validate book exists and has stock
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        
        if book.stock < quantity:
            raise ValueError("Insufficient stock")
        
        # Get or create cart
        cart = self.cart_repository.get_or_create_by_customer_id(customer_id)
        
        # Get or create cart item
        cart_item = self.cart_item_repository.get_or_create(
            cart_id=cart.id,
            book_id=book_id,
            quantity=quantity
        )
        
        # If item already exists, update quantity
        if cart_item.id != 0:  # Item already existed
            cart_item.quantity += quantity
            self.cart_item_repository.update(cart_item)
        
        return cart


class ViewCartUseCase:
    """View cart contents"""
    
    def __init__(
        self,
        cart_repository: ICartRepository,
        cart_item_repository: ICartItemRepository,
        customer_repository: ICustomerRepository
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.customer_repository = customer_repository
    
    def execute(self, customer_id: int) -> Tuple[Optional[Cart], List[CartItem]]:
        # Validate customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Get cart
        cart = self.cart_repository.get_by_customer_id(customer_id)
        if not cart:
            return None, []
        
        # Get cart items
        items = self.cart_item_repository.get_by_cart_id(cart.id)
        
        return cart, items
