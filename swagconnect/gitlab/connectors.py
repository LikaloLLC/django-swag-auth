from swagconnect.oauth2.views import CustomOAuth2Adapter


class GitlabConnector(CustomOAuth2Adapter):
    id = 'gitlab'
