from rest_framework import serializers

from apps.ausers.serializers import UserDetailSerializer
from apps.books.serializers import BookSerializer

from apps.orders.models import Order


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "created_time", "user", "book", "due_date"]
        read_only_fields = ["id", "created_time"]

    def validate(self, data):
        book = data.get("book")

        if book and book.available:
            return data

        raise serializers.ValidationError("Book is already booked or not available")


class OrderSerializer(CreateOrderSerializer):

    class Meta(CreateOrderSerializer.Meta):
        fields = CreateOrderSerializer.Meta.fields + ["return_date", "fine"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update({
            "user": UserDetailSerializer(instance.user).data,
            "book": BookSerializer(instance.book).data,
            "calculate_fine": instance.calculate_fine(),
        })
        return rep


class CompleteReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "return_date"]

    def validate(self, data):
        return_date = data.get("return_date")

        if not return_date:
            raise serializers.ValidationError({"return_date": "return_date is required"})

        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update({
            "user": UserDetailSerializer(instance.user).data,
            "book": BookSerializer(instance.book).data,
            "fine": instance.fine,
            "calculate_fine": instance.calculate_fine(),
        })
        return rep

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.mark_as_returned()  # Kitobni qaytarish va mavjud qilish
        return instance
