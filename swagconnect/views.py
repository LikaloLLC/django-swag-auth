from rest_framework.viewsets import ModelViewSet

from .serializers import SwaggerStorageSerializer


class SwaggerStorageViewSet(ModelViewSet):
    serializer_class = SwaggerStorageSerializer

    # TODO:
    #  1. Must accept only authenticated users (https://www.django-rest-framework.org/api-guide/authentication/)
    #  2. Must pass current user to the model on save, which can be found in request.user (look at `.perform_create()`)
    #  3. Add the remaining attributes to this viewset (https://www.django-rest-framework.org/api-guide/viewsets/)
    #  This endpoint accepts ConnectorToken PK and url to the swagger. For testing, you should authenticate via github,
    #  copy the PK of the ConnectorToken and pass it to this endpoint.
