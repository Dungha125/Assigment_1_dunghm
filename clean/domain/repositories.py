"""
Repository interfaces - Define contracts for data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Customer, Book, Cart, CartItem


class ICustomerRepository(ABC):
    """Customer repository interface"""
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass


class IBookRepository(ABC):
    """Book repository interface"""
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass


class ICartRepository(ABC):
    """Cart repository interface"""
    
    @abstractmethod
    def create(self, cart: Cart) -> Cart:
        pass
    
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        pass
    
    @abstractmethod
    def get_or_create_by_customer_id(self, customer_id: int) -> Cart:
        pass


class ICartItemRepository(ABC):
    """CartItem repository interface"""
    
    @abstractmethod
    def create(self, cart_item: CartItem) -> CartItem:
        pass
    
    @abstractmethod
    def get_by_cart_and_book(self, cart_id: int, book_id: int) -> Optional[CartItem]:
        pass
    
    @abstractmethod
    def get_or_create(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        pass
    
    @abstractmethod
    def get_by_cart_id(self, cart_id: int) -> List[CartItem]:
        pass
    
    @abstractmethod
    def update(self, cart_item: CartItem) -> CartItem:
        pass
