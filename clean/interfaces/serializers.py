"""
Serializers for API responses
"""
from dataclasses import asdict
from typing import List
from domain.entities import Customer, Book, Cart, CartItem


class CustomerSerializer:
    """Customer serializer"""
    
    @staticmethod
    def to_dict(customer: Customer, include_password: bool = False) -> dict:
        data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }
        if include_password:
            data['password'] = customer.password
        return data


class BookSerializer:
    """Book serializer"""
    
    @staticmethod
    def to_dict(book: Book) -> dict:
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock': book.stock
        }
    
    @staticmethod
    def to_dict_list(books: List[Book]) -> List[dict]:
        return [BookSerializer.to_dict(book) for book in books]


class CartItemSerializer:
    """CartItem serializer"""
    
    @staticmethod
    def to_dict(cart_item: CartItem, book: Book = None) -> dict:
        data = {
            'id': cart_item.id,
            'book_id': cart_item.book_id,
            'quantity': cart_item.quantity
        }
        if book:
            data['book'] = BookSerializer.to_dict(book)
        return data


class CartSerializer:
    """Cart serializer"""
    
    @staticmethod
    def to_dict(cart: Cart, items: List[CartItem] = None, books: List[Book] = None) -> dict:
        data = {
            'id': cart.id,
            'customer_id': cart.customer_id,
            'created_at': cart.created_at.isoformat() if hasattr(cart.created_at, 'isoformat') else str(cart.created_at),
            'items': []
        }
        
        if items:
            book_dict = {book.id: book for book in (books or [])}
            data['items'] = [
                CartItemSerializer.to_dict(
                    item, 
                    book_dict.get(item.book_id)
                ) for item in items
            ]
        
        return data
