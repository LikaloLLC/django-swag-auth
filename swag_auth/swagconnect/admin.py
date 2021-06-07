from django.contrib import admin

from swag_auth.swagconnect.models import SwaggerStorage, ConnectorToken

admin.site.register(ConnectorToken)
admin.site.register(SwaggerStorage)
