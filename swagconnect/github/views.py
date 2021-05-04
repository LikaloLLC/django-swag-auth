from swagconnect.oauth2.views import OAuth2LoginView, OAuth2CallbackView, CustomOAuth2Adapter

oauth_login = OAuth2LoginView.adapter_view(CustomOAuth2Adapter)
oauth_callback = OAuth2CallbackView.adapter_view(CustomOAuth2Adapter)
