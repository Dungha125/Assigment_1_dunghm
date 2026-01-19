from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:customer_id>/', views.add_to_cart, name='add_to_cart'),
    path('view/<int:customer_id>/', views.view_cart, name='view_cart'),
]
