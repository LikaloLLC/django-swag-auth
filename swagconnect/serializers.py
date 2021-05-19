from rest_framework import serializers

from .models import SwaggerStorage


class SwaggerStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwaggerStorage
        fields = ('user', 'url', 'token')
