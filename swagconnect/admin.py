from django.contrib import admin
from swagconnect.models import SwaggerStorage, ConnectorToken

# Register your models here.

admin.site.register(ConnectorToken)
admin.site.register(SwaggerStorage)