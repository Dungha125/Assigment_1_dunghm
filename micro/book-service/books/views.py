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


@api_view(['GET'])
def get_books_by_ids(request):
    """Get multiple books by IDs (for other services)"""
    book_ids = request.GET.getlist('ids')
    if not book_ids:
        return Response({'error': 'No book IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book_ids = [int(id) for id in book_ids]
        books = Book.objects.filter(id__in=book_ids)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({'error': 'Invalid book IDs'}, status=status.HTTP_400_BAD_REQUEST)
