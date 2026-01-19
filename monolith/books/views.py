from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def book_list(request):
    """View book catalog"""
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def book_detail(request, book_id):
    """Get book details"""
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
