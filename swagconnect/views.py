from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import SwaggerStorage
from .serializers import SwaggerStorageSerializer


class SwaggerStorageViewSet(ModelViewSet):
    serializer_class = SwaggerStorageSerializer
    queryset = SwaggerStorage.objects.all()

    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

