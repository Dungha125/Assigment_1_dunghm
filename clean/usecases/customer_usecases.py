"""
Customer use cases
"""
from typing import Optional
from domain.entities import Customer
from domain.repositories import ICustomerRepository
from django.contrib.auth.hashers import make_password, check_password


class RegisterCustomerUseCase:
    """Register a new customer"""
    
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository
    
    def execute(self, name: str, email: str, password: str) -> Customer:
        # Check if email already exists
        existing = self.customer_repository.get_by_email(email)
        if existing:
            raise ValueError("Email already exists")
        
        # Create customer with hashed password
        hashed_password = make_password(password)
        customer = Customer(
            id=None,
            name=name,
            email=email,
            password=hashed_password
        )
        
        return self.customer_repository.create(customer)


class LoginCustomerUseCase:
    """Login customer"""
    
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository
    
    def execute(self, email: str, password: str) -> Optional[Customer]:
        customer = self.customer_repository.get_by_email(email)
        if not customer:
            return None
        
        if check_password(password, customer.password):
            return customer
        
        return None
