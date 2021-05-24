from django.urls import path, include
from swagconnect.github.views import GithubLogin

from swagconnect.bitbucket.views import oauth_callback as bitbucket_callback
from swagconnect.bitbucket.views import oauth_login as bitbucket_login
from swagconnect.github.views import oauth_callback as github_callback
from swagconnect.github.views import oauth_login as github_login
from swagconnect.gitlab.views import oauth_callback as gitlab_callback
from swagconnect.gitlab.views import oauth_login as gitlab_login
from swagconnect.views import SwaggerStorageViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', SwaggerStorageViewSet)

urlpatterns = [
    # # Bitbucket
    # path('bitbucket/login/', bitbucket_login, name='bitbucket_login'),
    # path('bitbucket/callback/', bitbucket_callback, name='bitbucket_callback'),
    #
    # # Github
    # path('github/login/', github_login, name='github_login'),
    # path('github/callback/', github_callback, name='github_callback'),
    #
    # # Gitlab
    # path('gitlab/login/', gitlab_login, name='gitlab_login'),
    # path('gitlab/callback/', gitlab_callback, name='gitlab_callback'),
    path('swagger_storage/', include(router.urls)),

    path('rest-auth/github/', GithubLogin.as_view(), name='github_login')
]
