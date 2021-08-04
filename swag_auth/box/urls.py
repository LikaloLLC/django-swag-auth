from swag_auth.oauth2.urls import default_urlpatterns

from .connectors import BoxConnector

conn_urlpatterns = default_urlpatterns(BoxConnector)
