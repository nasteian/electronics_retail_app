from rest_framework import serializers
from api.models import RetailObject, Product, Contact, Address


class RetailObjectSerializer(serializers.ModelSerializer):
    debt = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = RetailObject
        fields = "__all__"


class ProductObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AddressObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ContactObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "email",
        ]
