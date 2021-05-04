from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter


class CustomOAuth2Adapter(OAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return

    def get_provider(self):
        return


# TODO: OAuth2View and OAuth2CallbackView
