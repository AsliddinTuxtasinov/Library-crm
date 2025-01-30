from rest_framework import views, generics

from apps.ausers.enums import UserRolesChoices
from apps.ausers.permissions import UserPermission, UserAndOperatorPermission
from apps.orders.models import Reservation
from apps.orders.serializers import CreateBookedSerializer, BookedSerializer
from core.base.utils import CustomPagination


class CreateBookedView(generics.CreateAPIView):
    permission_classes = [UserPermission]
    serializer_class = CreateBookedSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListBookedView(generics.ListAPIView):
    queryset = Reservation.objects.select_related("book", "user").all()
    permission_classes = [UserAndOperatorPermission]
    serializer_class = BookedSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.user_roles == UserRolesChoices.USER:
            return self.queryset.filter(user=self.request.user)
        return self.queryset
