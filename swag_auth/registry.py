import importlib
from collections import OrderedDict

from django.conf import settings


class ConnectorRegistry(object):
    def __init__(self, module_name: str):
        self.connector_map = OrderedDict()
        self.loaded = False

        self.module_name = module_name

    def get_list(self, request=None):
        self.load()
        return [connector_cls(request) for connector_cls in self.connector_map.values()]

    def register(self, cls):
        self.connector_map[cls.provider_id] = cls

    def by_id(self, provider_id, request=None):
        self.load()
        return self.connector_map[provider_id](request=request)

    def as_choices(self):
        self.load()
        for connector_cls in self.connector_map.values():
            yield (connector_cls.provider_id, connector_cls.provider_id)

    def load(self):
        # TODO: connectors register with the connectors registry when
        # loaded. Here, we build the URLs for all registered connectors. So, we
        # really need to be sure all connectors did register, which is why we're
        # forcefully importing the `connector` modules here. The overall
        # mechanism is way to magical and depends on the import order et al, so
        # all of this really needs to be revisited.

        if not self.loaded:
            for app in settings.INSTALLED_APPS:
                try:
                    if not app.startswith(self.module_name):
                        continue
                    connector_module = importlib.import_module(f'{app}.connectors')
                except ImportError:
                    pass
                else:
                    for cls in getattr(connector_module, "connector_classes", []):
                        self.register(cls)
            self.loaded = True


connector_registry = ConnectorRegistry('swag_auth')
