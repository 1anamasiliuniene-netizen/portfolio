from .models import Project


def nav_projects(request):
    return {
        "nav_projects": Project.objects.filter(is_published=True).order_by("order")
    }
