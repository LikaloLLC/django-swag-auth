from importlib import import_module

from django.urls import include, path
from rest_framework import routers

from swag_auth import registry
from swag_auth.views import SwaggerStorageViewSet

router = routers.SimpleRouter()
router.register(r'', SwaggerStorageViewSet)

urlpatterns = [
    path('swagger_storage/', include(router.urls)),
]

for connector in registry.connector_registry.get_list():
    try:
        prov_mod = import_module(connector.get_package() + ".urls")
    except ImportError:
        continue
    else:
        urlpatterns += getattr(prov_mod, "conn_urlpatterns", [])
