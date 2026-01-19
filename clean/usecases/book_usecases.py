"""
Book use cases
"""
from typing import List, Optional
from domain.entities import Book
from domain.repositories import IBookRepository


class GetBookCatalogUseCase:
    """Get all books"""
    
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository
    
    def execute(self) -> List[Book]:
        return self.book_repository.get_all()


class GetBookByIdUseCase:
    """Get book by ID"""
    
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository
    
    def execute(self, book_id: int) -> Optional[Book]:
        return self.book_repository.get_by_id(book_id)
