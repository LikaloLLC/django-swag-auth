from swag_auth.oauth2.urls import default_urlpatterns

from .connectors import BitbucketConnector

conn_urlpatterns = default_urlpatterns(BitbucketConnector)
