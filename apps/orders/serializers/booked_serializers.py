from rest_framework import serializers

from apps.ausers.serializers import UserDetailSerializer
from apps.books.serializers import BookSerializer
from apps.orders.models import Reservation


class CreateBookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "created_time", "user", "book", "reserved_at"]
        read_only_fields = ["id", "created_time", "user"]

    def validate(self, data):
        book = data.get("book")

        if book and book.available:
            return data

        raise serializers.ValidationError("Book is already booked or not available")


class BookedSerializer(CreateBookedSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update({
            "user": UserDetailSerializer(instance.user).data,
            "book": BookSerializer(instance.book).data,
        })
        return rep
