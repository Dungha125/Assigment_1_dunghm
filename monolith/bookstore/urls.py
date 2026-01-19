"""
URL configuration for bookstore project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    """Display API endpoints information"""
    return JsonResponse({
        'message': 'Bookstore API - Monolithic Version',
        'endpoints': {
            'accounts': {
                'register': 'POST /api/accounts/register/',
                'login': 'POST /api/accounts/login/',
            },
            'books': {
                'list': 'GET /api/books/',
                'detail': 'GET /api/books/<id>/',
            },
            'cart': {
                'add': 'POST /api/cart/add/<customer_id>/',
                'view': 'GET /api/cart/view/<customer_id>/',
            },
            'admin': 'GET /admin/',
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
    path('api/cart/', include('cart.urls')),
]
