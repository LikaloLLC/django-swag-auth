from typing import Optional

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from swag_auth.models import SwaggerStorage, ConnectorToken
from swag_auth.serializers import SwaggerStorageSerializer


class SwaggerStorageViewSet(ModelViewSet):
    serializer_class = SwaggerStorageSerializer
    queryset = SwaggerStorage.objects.all()

    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        return SwaggerStorage.objects.filter(user=user)

    def get_existing_storage(self, token_pk: str, url: str) -> Optional['SwaggerStorage']:
        """Return SwaggerStorage, filtered by the specified user, url and token__connector, if exists."""
        token = ConnectorToken.objects.get(pk=token_pk)

        return SwaggerStorage.objects.filter(
            user=self.request.user, url=url, token__connector=token.connector
        ).last()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user already has a SwaggerStorage instance with the specified url and provider.
        # If it exists, just update it with a new token,
        # so we don't create multiple identical records.
        existing_storage = self.get_existing_storage(request.data['token'], request.data['url'])
        if existing_storage:
            serializer = self.get_serializer(existing_storage, data={'token': serializer.data['token']})
            serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
