from rest_framework import generics

from apps.ausers.permissions import OperatorPermission
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer, CreateOrderSerializer, CompleteReservationSerializer
from core.base.utils import CustomPagination


class ListCreateOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all().select_related("user", "book")

    serializer_class = OrderSerializer
    create_serializer_class = CreateOrderSerializer

    permission_classes = [OperatorPermission]
    pagination_class = CustomPagination

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return self.serializer_class

        return self.create_serializer_class


class RetrieveUpdateOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().select_related("user", "book")

    serializer_class = OrderSerializer
    update_serializer_class = CompleteReservationSerializer

    permission_classes = [OperatorPermission]
    http_method_names = ["get", "patch"]
    lookup_url_kwarg = "order_id"

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return self.serializer_class

        return self.update_serializer_class
