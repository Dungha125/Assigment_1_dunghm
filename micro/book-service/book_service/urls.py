"""
URL configuration for book-service
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    """Display API endpoints information"""
    return JsonResponse({
        'message': 'Book Service API - Microservices Architecture',
        'service': 'book-service',
        'port': 8002,
        'endpoints': {
            'list': 'GET /api/books/',
            'detail': 'GET /api/books/<id>/',
            'batch': 'GET /api/books/batch/?ids=1&ids=2',
            'admin': 'GET /admin/',
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
]
