from django.db import migrations


def seed_public_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")

    projects = [
        {
            "title": "A Terapija",
            "slug": "a-terapija",
            "subtitle": "UX research, product design and Django development",
            "summary": (
                "A digital wellbeing platform shaped through discovery, user research, "
                "information architecture, responsive design and Django implementation."
            ),
            "is_published": True,
            "order": 1,
            "live_url": "https://www.a-terapija.lt",
            "source_url": "https://github.com/1anamasiliuniene-netizen/A-Terapija.git",
        },
        {
            "title": "Mini Notion",
            "slug": "mini-notion",
            "subtitle": "Productivity dashboard and task workflow redesign",
            "summary": (
                "A project-management case study focused on dashboard clarity, task "
                "flows, information hierarchy, design proposals and interface refinement."
            ),
            "is_published": True,
            "order": 2,
            "live_url": "https://mini-notion-anama.pythonanywhere.com/projects/",
            "source_url": "https://github.com/1anamasiliuniene-netizen/mini_notion",
        },
    ]

    for project in projects:
        Project.objects.update_or_create(
            slug=project["slug"],
            defaults=project,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0009_project_live_url_project_source_url"),
    ]

    operations = [
        migrations.RunPython(
            seed_public_projects,
            migrations.RunPython.noop,
        ),
    ]
