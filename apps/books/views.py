from rest_framework import generics, permissions

from apps.ausers.permissions import OperatorPermission
from apps.books.models import Genre, Author, Book
from apps.books.serializers import GenreSerializer, AuthorSerializer, BookSerializer, CreateUpdateBookSerializer
from core.base.utils import CustomPagination


class ListCreateGenreView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination
    permission_classes = [OperatorPermission]


class ListCreateAuthorView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPagination
    permission_classes = [OperatorPermission]


class ListCreateBookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    pagination_class = CustomPagination

    create_serializer_class = CreateUpdateBookSerializer
    serializer_class = BookSerializer

    def get_serializer_class(self):
        """ POST uchun `CreateUpdateBookSerializer`, GET uchun `BookSerializer` """

        if self.request.method == "POST":
            return self.create_serializer_class

        return self.serializer_class

    def get_permissions(self):
        """ POST uchun `OperatorPermission`, GET uchun `IsAuthenticated` """

        if self.request.method == "POST":
            return [OperatorPermission()]

        return [permissions.IsAuthenticated()]


class RetrieveUpdateDestroyBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    pagination_class = CustomPagination

    create_serializer_class = CreateUpdateBookSerializer
    serializer_class = BookSerializer

    http_method_names = ['get', 'patch', 'delete']
    lookup_url_kwarg = "book_id"

    def get_serializer_class(self):

        if self.request.method == "GET":
            return self.serializer_class

        return self.create_serializer_class

    def get_permissions(self):

        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]

        return [OperatorPermission()]
