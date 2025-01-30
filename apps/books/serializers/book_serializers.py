from rest_framework import serializers

from apps.books.models import Book, Author, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]
        read_only_fields = ["id"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "created_time", "first_name", "last_name", "birth_date", "biography"]
        read_only_fields = ["id", "created_time"]


class CreateUpdateBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["id", "created_time", "title", "author", "genre", "daily_price", "available"]
        read_only_fields = ["id", "created_time"]


class BookSerializer(CreateUpdateBookSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update({
            "genre": GenreSerializer(instance.genre).data,
            "author": AuthorSerializer(instance.author).data,
        })
        return rep

