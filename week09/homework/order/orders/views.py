from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.response import Response
from orders.models import Orders
from .serializers import OrdersSerializer
from orders.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import filters
from django_filters import rest_framework as rf_filters
from django.http import HttpResponse


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def retrieve(self, request, pk=None):
        """ order详情 """
        # 获取实例
        user = self.get_object()
        # 序列化
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @api_view(['POST'])
    def create(self, request, *args, **kwargs):
        """
        创建order
        """
        serializer = OrdersSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'orders': reverse('order_list', request=request, format=format),
    })
