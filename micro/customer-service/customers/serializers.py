from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        customer = Customer.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer


class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']
