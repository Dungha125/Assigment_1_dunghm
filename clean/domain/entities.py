"""
Domain entities - Core business objects
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """Customer entity"""
    id: Optional[int]
    name: str
    email: str
    password: str

    def __post_init__(self):
        if self.id is None:
            self.id = 0


@dataclass
class Book:
    """Book entity"""
    id: Optional[int]
    title: str
    author: str
    price: float
    stock: int

    def __post_init__(self):
        if self.id is None:
            self.id = 0


@dataclass
class Cart:
    """Cart entity"""
    id: Optional[int]
    customer_id: int
    created_at: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = 0
        if not isinstance(self.created_at, datetime):
            self.created_at = datetime.now()


@dataclass
class CartItem:
    """CartItem entity"""
    id: Optional[int]
    cart_id: int
    book_id: int
    quantity: int

    def __post_init__(self):
        if self.id is None:
            self.id = 0
