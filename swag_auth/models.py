from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields.fields import EncryptedTextField

import swag_auth.registry as registry
from swag_auth.api_connector import BaseAPIConnector


class ConnectorToken(models.Model):
    # Must contain provider id
    connector = models.CharField(
        verbose_name=_("connector"),
        max_length=30,
    )

    token = EncryptedTextField(
        verbose_name=_("token"),
        help_text=_('"oauth_token" (OAuth1) or access token (OAuth2)'),
    )
    token_secret = EncryptedTextField(
        blank=True,
        verbose_name=_("token secret"),
        help_text=_('"oauth_token_secret" (OAuth1) or refresh token (OAuth2)'),
    )
    expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("expires at")
    )

    def __str__(self):
        return self.token

    def get_api_connector(self) -> 'BaseAPIConnector':
        """Return an initialized instance of API connector for the particular connector."""
        provider = registry.connector_registry.by_id(self.connector)

        return provider.api_connector_class(self.token)


class SwaggerStorage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('url'),
        help_text=_('Swagger URL')
    )
    token = models.ForeignKey(
        ConnectorToken,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('token')
    )

    def get_file(self):
        """Return content of the file, specified in the url field."""
        api_connector = self.token.get_api_connector()

        return api_connector.get_swagger(self.url)
