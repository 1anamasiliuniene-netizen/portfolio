from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import AdditionalCertificate, ContactLink, Project, ResumeDocument

def a_terapija(request):
    return render(request, 'portfolio/project_detail.html')


def about(request):
    contact_links = ContactLink.objects.filter(is_active=True)

    return render(
        request,
        'portfolio/about.html',
        {
            "contact_links": contact_links,
        },
    )


class ProjectListView(ListView):

    model = Project

    template_name = "portfolio/projects.html"

    context_object_name = "projects"

    def get_queryset(self):

        return (

            Project.objects

            .filter(is_published=True)

            .order_by("order")

        )

class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Project.objects
            .filter(is_published=True)
            .prefetch_related(
                "case_study_sections__expandables",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        context["previous_project"] = (
            Project.objects
            .filter(
                is_published=True,
                order__lt=project.order,
            )
            .order_by("-order")
            .first()
        )

        context["next_project"] = (
            Project.objects
            .filter(
                is_published=True,
                order__gt=project.order,
            )
            .order_by("order")
            .first()
        )

        return context


def resume(request):
    resume_document = (
        ResumeDocument.objects
        .filter(is_active=True)
        .first()
    )

    additional_certificates = (
        AdditionalCertificate.objects
        .filter(is_active=True)
    )

    return render(
        request,
        "portfolio/resume.html",
        {
            "resume_document": resume_document,
            "additional_certificates": additional_certificates,
        },
    )
