"""
URL configuration for cart-service
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    """Display API endpoints information"""
    return JsonResponse({
        'message': 'Cart Service API - Microservices Architecture',
        'service': 'cart-service',
        'port': 8003,
        'endpoints': {
            'add_to_cart': 'POST /api/cart/add/<customer_id>/',
            'view_cart': 'GET /api/cart/view/<customer_id>/',
            'admin': 'GET /admin/',
        },
        'dependencies': {
            'customer_service': 'http://localhost:8001',
            'book_service': 'http://localhost:8002',
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/cart/', include('carts.urls')),
]
