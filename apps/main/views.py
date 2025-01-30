from rest_framework import generics, permissions

from apps.ausers.permissions import UserPermission
from apps.main.models import Review
from apps.main.serializers import ReviewSerializer
from core.base.utils import CustomPagination


class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [UserPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListReviewsByBookIdView(generics.ListAPIView):
    queryset = Review.objects.all().select_related('book', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    lookup_field = 'book_id'

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return self.queryset.filter(book_id=book_id)
