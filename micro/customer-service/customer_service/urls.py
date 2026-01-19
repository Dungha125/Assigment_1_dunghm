"""
URL configuration for customer-service
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    """Display API endpoints information"""
    return JsonResponse({
        'message': 'Customer Service API - Microservices Architecture',
        'service': 'customer-service',
        'port': 8001,
        'endpoints': {
            'register': 'POST /api/customers/register/',
            'login': 'POST /api/customers/login/',
            'get_customer': 'GET /api/customers/<id>/',
            'admin': 'GET /admin/',
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/customers/', include('customers.urls')),
]
