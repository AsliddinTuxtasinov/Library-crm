from rest_framework import serializers

from apps.ausers.serializers import UserDetailSerializer
from apps.main.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ["id", "created_time", "user", "book", "rating", "comment"]
        read_only_fields = ["id", "created_time", "user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update({
            "user": UserDetailSerializer(instance.user).data,
        })
        return rep
