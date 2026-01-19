"""
URL configuration for Clean Architecture bookstore project.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from . import views

def api_info(request):
    """Display API endpoints information"""
    return JsonResponse({
        'message': 'Bookstore API - Clean Architecture Version',
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
    path('api/accounts/register/', views.register, name='register'),
    path('api/accounts/login/', views.login, name='login'),
    path('api/books/', views.book_list, name='book_list'),
    path('api/books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('api/cart/add/<int:customer_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/view/<int:customer_id>/', views.view_cart, name='view_cart'),
]
