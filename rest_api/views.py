from core.models import *
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from core.models import Item, OrderItem, Order, Address
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from rest_framework import generics
from .serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, ContactSerializer


class ItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    model = Item
    queryset = Item.objects.all()
    lookup_field = 'slug'


class AddToCartView(CreateModelMixin, generics.GenericAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer()

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        item = get_object_or_404(Item, slug=slug)
        size = request.data.get('size')
        color = request.data.get('color')
        if OrderItem.objects.filter(
			item=item,
			user=request.user,
			ordered=False,
		):
            dels = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False,
			)
            for q in dels:
                q.delete()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save(user=request.user, ordered=False, size=size, color=color)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                message = "This item quantity was updated"
            else:
                order.items.add(order_item)
                message = "This item was added to your cart"
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            message = "This item was added to your cart"

        order_serializer = OrderSerializer(order)
        return Response({
            'message': message,
            'order': order_serializer.data
        }, status=status.HTTP_201_CREATED)
    
class CartAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if not order.items.exists():
                raise ObjectDoesNotExist("No items in cart")
            return order
        except ObjectDoesNotExist:
            return None


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({
                "message": "You do not have an active order"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
class ItemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_field = 'slug'
   

