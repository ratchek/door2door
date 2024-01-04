# tests.py

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from dashboard.views import index


class IndexViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="jacob", email="jacob@gmail.com", password="top_secret"
        )

    def test_index_view_authenticated_user(self):
        request = self.factory.get("/")
        request.user = self.user

        response = index(request)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(
            response, reverse("address-info"), fetch_redirect_response=False
        )

    def test_index_view_unauthenticated_user(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = index(request)
        self.assertEqual(response.status_code, 200)  # Expecting a success status code
