from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders import views
from orders.views import OrdersViewSet
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls

#  路径                       功能
# /orders               列出所有 order
# /orders/{id}          列出具体的一个订单
# /orders/create        只接受 Post 请求创建一个订单
# /orders/{id}/cancel   接受 Get 请求，取消一个订单。

orders_list = OrdersViewSet.as_view({
    'get': 'list'
})

orders_detail = OrdersViewSet.as_view({
    'get': 'retrieve',
})


orders_cancel = OrdersViewSet.as_view({
    'get': 'cancel'
})

router = DefaultRouter()
router.register(r'', views.OrdersViewSet, 'order_list')

urlpatterns = [
    path('', orders_list, name='orders-list'),
    path('/<int:pk>', orders_detail, name='orders-detail'),
    path('/create', include(router.urls)),
    path('/<int:pk>/cancel', orders_cancel, name='orders-cancel'),
    # path('api-auth/', include('rest_framework.urls',
    #                           namespace='rest_framework')),
]
