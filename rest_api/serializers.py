from core.models import *
from rest_framework import serializers


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = '__all__'


class SizeInstanceSerializer(serializers.ModelSerializer):
    size_cloth = SizeSerializer(many=True)
    class Meta:
        model = Size_Instance
        fields = '__all__'


class ColorInstanceSerializer(serializers.ModelSerializer):
    color_cloth = ColorSerializer(many=True)
    class Meta:
        model = Color_Instance
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    sizes_of_items = SizeInstanceSerializer()
    color_of_items = ColorInstanceSerializer()

    class Meta:
        model = Item
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'       

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    payment = PaymentSerializer()
    shipping_address = AddressSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'