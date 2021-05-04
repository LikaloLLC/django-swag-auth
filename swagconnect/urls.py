from django.urls import path

from swagconnect.github.views import oauth_login as github_login
from swagconnect.github.views import oauth_callback as github_callback

#
# urlpatterns = [
#     path('github/login/', github_login),
#     path('github/callback/', github_callback),
# ]