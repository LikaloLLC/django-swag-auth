import json
import os
from abc import abstractmethod, ABC
from typing import Union, Type

import yaml
from django.core.exceptions import ValidationError


class BaseAPIConnector(ABC):
    def __init__(self, token):
        self._token = token

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    @abstractmethod
    def get_file_content(self, *args, **kwargs):
        """
        Return content of the given file
        """
        pass


class BaseSwaggerDownloader(ABC):
    api_connector_cls: Type['BaseAPIConnector'] = None

    # A mapping of extension name to a real loader
    loaders = {
        'json': json.loads,
        'yml': yaml.safe_load,
        'yaml': yaml.safe_load
    }

    def __init__(self, token):
        if (
            self.api_connector_cls is None
            or not issubclass(self.api_connector_cls, BaseAPIConnector)
        ):
            raise TypeError(
                'parameter `api_connector` must not be None '
                'and must be a subclass of `BaseAPIConnector`'
            )

        self._token = token

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    def get_api_connector(self):
        return self.api_connector_cls(self._token)

    def get_swagger(self, url: str) -> dict:
        api_connector = self.get_api_connector()

        contents = self.get_swagger_content(url, api_connector)
        extension = self.get_extension(url)

        if not self.is_valid(extension):
            raise ValidationError("File content type must be JSON, YAML or YML")

        return self.get_swagger_data(extension, contents)

    @abstractmethod
    def get_swagger_content(self, url, connector):
        pass

    def get_extension(self, url: str):
        return os.path.splitext(url)[1][1:]

    def get_swagger_data(self, extension: str, contents: Union[str, bytes]) -> dict:
        return self.loaders[extension](contents)

    def is_valid(self, extension: str) -> bool:
        """Validate path to YAML or JSON"""
        return extension in self.loaders
