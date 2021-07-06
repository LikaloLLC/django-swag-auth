from django.urls import path, include
from rest_framework import routers

from swag_auth.bitbucket.views import oauth_callback as bitbucket_callback
from swag_auth.bitbucket.views import oauth_login as bitbucket_login
from swag_auth.github.views import oauth_callback as github_callback
from swag_auth.github.views import oauth_login as github_login
from swag_auth.gitlab.views import oauth_callback as gitlab_callback
from swag_auth.gitlab.views import oauth_login as gitlab_login
from swag_auth.google_drive.views import oauth_callback as google_callback
from swag_auth.google_drive.views import oauth_login as google_login
from swag_auth.views import SwaggerStorageViewSet

router = routers.SimpleRouter()
router.register(r'', SwaggerStorageViewSet)

urlpatterns = [
    # Bitbucket
    path('bitbucket/login/', bitbucket_login, name='bitbucket_login'),
    path('bitbucket/callback/', bitbucket_callback, name='bitbucket_callback'),

    # Github
    path('github/login/', github_login, name='github_login'),
    path('github/callback/', github_callback, name='github_callback'),

    # Gitlab
    path('gitlab/login/', gitlab_login, name='gitlab_login'),
    path('gitlab/callback/', gitlab_callback, name='gitlab_callback'),
    path('swagger_storage/', include(router.urls)),

    # Google drive
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
]
