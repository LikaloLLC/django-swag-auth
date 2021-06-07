from django.shortcuts import reverse
from django.test import TestCase


class Oauth2Test(TestCase):
    def test_github_login(self):
        url = reverse('github_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_github_callback_url(self):
        url = reverse('github_callback')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_gitlab_login(self):
        url = reverse('gitlab_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_gitlab_callback_url(self):
        url = reverse('gitlab_callback')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_bitbucket_login(self):
        url = reverse('bitbucket_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_bitbucket_callback_url(self):
        url = reverse('bitbucket_callback')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
