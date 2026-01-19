"""
Repository implementations using Django ORM
"""
from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem
from domain.repositories import (
    ICustomerRepository, IBookRepository,
    ICartRepository, ICartItemRepository
)
from framework.models import CustomerModel, BookModel, CartModel, CartItemModel
from datetime import datetime


class CustomerRepository(ICustomerRepository):
    """Customer repository implementation"""
    
    def create(self, customer: Customer) -> Customer:
        model = CustomerModel.objects.create(
            name=customer.name,
            email=customer.email,
            password=customer.password
        )
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password
        )
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return Customer(
                id=model.id,
                name=model.name,
                email=model.email,
                password=model.password
            )
        except CustomerModel.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(email=email)
            return Customer(
                id=model.id,
                name=model.name,
                email=model.email,
                password=model.password
            )
        except CustomerModel.DoesNotExist:
            return None


class BookRepository(IBookRepository):
    """Book repository implementation"""
    
    def get_all(self) -> List[Book]:
        models = BookModel.objects.all()
        return [
            Book(
                id=model.id,
                title=model.title,
                author=model.author,
                price=float(model.price),
                stock=model.stock
            )
            for model in models
        ]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        try:
            model = BookModel.objects.get(id=book_id)
            return Book(
                id=model.id,
                title=model.title,
                author=model.author,
                price=float(model.price),
                stock=model.stock
            )
        except BookModel.DoesNotExist:
            return None


class CartRepository(ICartRepository):
    """Cart repository implementation"""
    
    def create(self, cart: Cart) -> Cart:
        model = CartModel.objects.create(
            customer_id=cart.customer_id,
            created_at=cart.created_at
        )
        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            created_at=model.created_at
        )
    
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        try:
            model = CartModel.objects.get(customer_id=customer_id)
            return Cart(
                id=model.id,
                customer_id=model.customer_id,
                created_at=model.created_at
            )
        except CartModel.DoesNotExist:
            return None
    
    def get_or_create_by_customer_id(self, customer_id: int) -> Cart:
        model, created = CartModel.objects.get_or_create(
            customer_id=customer_id,
            defaults={'created_at': datetime.now()}
        )
        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            created_at=model.created_at
        )


class CartItemRepository(ICartItemRepository):
    """CartItem repository implementation"""
    
    def create(self, cart_item: CartItem) -> CartItem:
        model = CartItemModel.objects.create(
            cart_id=cart_item.cart_id,
            book_id=cart_item.book_id,
            quantity=cart_item.quantity
        )
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            quantity=model.quantity
        )
    
    def get_by_cart_and_book(self, cart_id: int, book_id: int) -> Optional[CartItem]:
        try:
            model = CartItemModel.objects.get(cart_id=cart_id, book_id=book_id)
            return CartItem(
                id=model.id,
                cart_id=model.cart_id,
                book_id=model.book_id,
                quantity=model.quantity
            )
        except CartItemModel.DoesNotExist:
            return None
    
    def get_or_create(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        model, created = CartItemModel.objects.get_or_create(
            cart_id=cart_id,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        if not created:
            model.quantity += quantity
            model.save()
        
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            quantity=model.quantity
        )
    
    def get_by_cart_id(self, cart_id: int) -> List[CartItem]:
        models = CartItemModel.objects.filter(cart_id=cart_id)
        return [
            CartItem(
                id=model.id,
                cart_id=model.cart_id,
                book_id=model.book_id,
                quantity=model.quantity
            )
            for model in models
        ]
    
    def update(self, cart_item: CartItem) -> CartItem:
        model = CartItemModel.objects.get(id=cart_item.id)
        model.quantity = cart_item.quantity
        model.save()
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            quantity=model.quantity
        )
