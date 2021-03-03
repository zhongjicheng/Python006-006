from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
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


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, methods=['GET'])
    def cancel(self, request, *args, **kwargs):
        order = self.get_object()
        if order.is_cancel is False:
            order.is_cancel = True
            order.save()
            return Response({'status': '订单取消成功'})
        else:
            return Response({'status': '订单已取消, 请不要重复提交'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'orders': reverse('order_list', request=request, format=format),
    })
