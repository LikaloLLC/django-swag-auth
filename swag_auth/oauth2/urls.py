from allauth.utils import import_attribute
from django.urls import include, path


def default_urlpatterns(connector):
    login_view = import_attribute(connector.get_package() + ".views.oauth2_login")
    callback_view = import_attribute(connector.get_package() + ".views.oauth2_callback")

    urlpatterns = [
        path("login/", login_view, name=connector.provider_id + "_login"),
        path("login/callback/", callback_view, name=connector.provider_id + "_callback"),
    ]
    return [path(connector.get_slug() + "/", include(urlpatterns))]
