from rest_framework import serializers

from .models import SwaggerStorage


class SwaggerStorageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = SwaggerStorage
        fields = ('user', 'url', 'token')

