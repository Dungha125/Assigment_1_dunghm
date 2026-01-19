from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, CustomerLoginSerializer, CustomerResponseSerializer


@api_view(['POST'])
def register(request):
    """Customer registration"""
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerResponseSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """Customer login"""
    serializer = CustomerLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                response_serializer = CustomerResponseSerializer(customer)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_customer(request, customer_id):
    """Get customer by ID (for other services)"""
    try:
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerResponseSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
