# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import serializers
from .models import Orders
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response


class OrdersSerializer(serializers.ModelSerializer):
    """订单序列"""

    class Meta:
        model = Orders
        fields = ['id', 'product_id', 'product_name', 'product_size', 'quantity', 'price', 'total_amount', 'is_cancel']

    @api_view(['GET'])
    def show_data(self, request):
        id = request.GET['id']
        datas = Orders.objects.filter(article_id=id)
        order_data = OrdersSerializer(datas, many=True)
        return Response({'order_data': OrdersSerializer.data})

    @api_view(['POST'])
    def create_data(self, request):
        id = request.GET['id']
        datas = Orders.objects.filter(article_id=id)
        order_data = OrdersSerializer(datas, many=True)
        return Response({'order_data': OrdersSerializer.data})
