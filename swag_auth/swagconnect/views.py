from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from swag_auth.swagconnect.models import SwaggerStorage
from swag_auth.swagconnect.serializers import SwaggerStorageSerializer


class SwaggerStorageViewSet(ModelViewSet):
    serializer_class = SwaggerStorageSerializer
    queryset = SwaggerStorage.objects.all()

    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        return SwaggerStorage.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
