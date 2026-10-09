from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse


class LandingPageTests(SimpleTestCase):
    def test_root_redirects_to_projects(self):
        response = self.client.get("/", secure=True)

        self.assertRedirects(
            response,
            reverse("portfolio:projects_list"),
            fetch_redirect_response=False,
        )


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class PracticePageTests(TestCase):
    def test_client_page_uses_existing_contact_and_navigation(self):
        response = self.client.get(reverse("portfolio:build_practice"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/base.html")
        self.assertContains(response, "Dream big.")
        self.assertContains(response, 'href="/about/#contact"', count=3)
        self.assertContains(response, 'href="/projects/"')
        self.assertContains(response, 'width="2766" height="1634"')

    def test_projects_keeps_portfolio_and_adds_client_entry(self):
        from .models import Project
        Project.objects.create(title="Visible project", slug="visible-project", is_published=True)
        Project.objects.create(title="Private project", slug="private-project", is_published=False)
        response = self.client.get(reverse("portfolio:projects_list"))
        self.assertContains(response, "From research to working products")
        self.assertContains(response, 'href="/build-your-practice/"', count=2)
        self.assertContains(response, "Visible project")
        self.assertNotContains(response, "Private project")
