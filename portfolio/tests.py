from django.test import SimpleTestCase
from django.urls import reverse


class LandingPageTests(SimpleTestCase):
    def test_root_redirects_to_projects(self):
        response = self.client.get("/", secure=True)

        self.assertRedirects(
            response,
            reverse("portfolio:projects_list"),
            fetch_redirect_response=False,
        )
