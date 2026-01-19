"""
Service layer for communicating with other microservices
"""
import requests
from django.conf import settings


class CustomerService:
    """Client for customer-service"""
    
    @staticmethod
    def get_customer(customer_id):
        """Get customer from customer-service"""
        try:
            url = f"{settings.CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None


class BookService:
    """Client for book-service"""
    
    @staticmethod
    def get_book(book_id):
        """Get book from book-service"""
        try:
            url = f"{settings.BOOK_SERVICE_URL}/api/books/{book_id}/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def get_books_by_ids(book_ids):
        """Get multiple books from book-service"""
        try:
            url = f"{settings.BOOK_SERVICE_URL}/api/books/batch/"
            params = [('ids', book_id) for book_id in book_ids]
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.RequestException:
            return []
