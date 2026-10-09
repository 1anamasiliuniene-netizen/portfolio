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

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class ImageViewingTests(TestCase):
    def test_admin_images_are_individually_opt_in(self):
        from .models import Project, CaseStudySection
        project = Project.objects.create(title="Evidence", slug="evidence")
        section = CaseStudySection.objects.create(project=project, title="Comparison",
            large_image="large.png", small_image="small.png")
        url = reverse("portfolio:project_detail", args=[project.slug])
        self.assertNotContains(self.client.get(url), 'class="pf-image-zoom"')
        section.large_image_allow_full_size = True
        section.save()
        response = self.client.get(url)
        self.assertContains(response, 'class="pf-image-zoom"', count=1)
        self.assertContains(response, 'href="/media/large.png"')
        self.assertNotContains(response, 'href="/media/small.png"')
        section.small_image_allow_full_size = True
        section.save()
        self.assertContains(self.client.get(url), 'class="pf-image-zoom"', count=2)

    def test_legacy_images_are_selective(self):
        from .models import Project
        for slug, count in [("a-terapija", 4), ("mini-notion", 8)]:
            Project.objects.get_or_create(slug=slug, defaults={"title": slug})
            self.assertContains(self.client.get(reverse("portfolio:project_detail", args=[slug])),
                                'class="pf-image-zoom"', count=count)

    def test_examples_and_portrait_do_not_enlarge(self):
        response = self.client.get(reverse("portfolio:build_practice"))
        self.assertNotContains(response, 'class="pf-image-zoom"')
        self.assertNotContains(response, 'Select the image')
        self.assertNotContains(response, 'aria-label="View the')
        self.assertNotContains(self.client.get(reverse("portfolio:about")), 'class="pf-image-zoom"')

    def test_project_preview_controls(self):
        from .models import Project
        from .admin import ProjectAdmin
        from django.contrib.admin.sites import AdminSite
        project = Project.objects.create(title="Uploaded", slug="uploaded", desktop_image="desktop.png", responsive_image="responsive.png")
        url = reverse("portfolio:project_detail", args=[project.slug])
        self.assertNotContains(self.client.get(url), 'class="pf-image-zoom"')
        project.desktop_image_allow_full_size = True
        project.save()
        self.assertContains(self.client.get(url), 'class="pf-image-zoom"', count=1)
        project.responsive_image_allow_full_size = True
        project.save()
        self.assertContains(self.client.get(url), 'class="pf-image-zoom"', count=2)
        fields = ProjectAdmin(Project, AdminSite()).get_form(None).base_fields
        self.assertIn("desktop_image_allow_full_size", fields)
        self.assertIn("responsive_image_allow_full_size", fields)
