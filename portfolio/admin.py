from django.contrib import admin

from .models import (
    AdditionalCertificate,
    Project,
    CaseStudySection,
    CaseStudyExpandable,
    ContactLink,
    ResumeDocument,
)


class CaseStudyExpandableInline(admin.StackedInline):
    model = CaseStudyExpandable
    extra = 1
    ordering = ("order",)
    fields = (
        "order",
        "number",
        "summary",
        "content",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "is_published",
        "order",
    )

    list_editable = (
        "is_published",
        "order",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    fieldsets = (
        (
            "Project",
            {
                "fields": (
                    "title",
                    "slug",
                    "subtitle",
                    "summary",
                    "is_published",
                    "order",
                ),
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "live_url",
                    "source_url",
                ),
            },
        ),
        (
            "Images",
            {
                "fields": (
                    "cover_image",
                    "desktop_image",
                    "responsive_image",
                ),
            },
        ),
    )


@admin.register(CaseStudySection)
class CaseStudySectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "section_number",
        "order",
    )

    list_filter = (
        "project",
    )

    search_fields = (
        "title",
        "eyebrow",
        "project__title",
    )

    ordering = (
        "project",
        "order",
    )

    fieldsets = (
        (
            "Section",
            {
                "fields": (
                    "project",
                    "order",
                    "section_number",
                    "eyebrow",
                    "title",
                    "introduction",
                ),
            },
        ),
        (
            "Large image",
            {
                "fields": (
                    "large_image",
                    "large_image_alt",
                    "large_image_caption",
                ),
            },
        ),
        (
            "Small image",
            {
                "fields": (
                    "small_image",
                    "small_image_alt",
                    "small_image_caption",
                ),
            },
        ),
        (
            "Closing block",
            {
                "fields": (
                    "closing_label",
                    "closing_text",
                ),
            },
        ),
    )

    inlines = [
        CaseStudyExpandableInline,
    ]


@admin.register(CaseStudyExpandable)
class CaseStudyExpandableAdmin(admin.ModelAdmin):
    list_display = (
        "summary",
        "section",
        "number",
        "order",
    )

    list_filter = (
        "section__project",
        "section",
    )

    search_fields = (
        "summary",
        "section__title",
        "section__project__title",
    )

    ordering = (
        "section",
        "order",
    )


@admin.register(ResumeDocument)
class ResumeDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "uploaded_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    readonly_fields = (
        "uploaded_at",
    )


@admin.register(AdditionalCertificate)
class AdditionalCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "issuer",
        "is_active",
        "order",
        "uploaded_at",
    )

    list_editable = (
        "is_active",
        "order",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "issuer",
    )

    readonly_fields = (
        "uploaded_at",
    )

    ordering = (
        "order",
        "title",
    )


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "url",
        "is_active",
        "opens_in_new_tab",
        "order",
    )

    list_editable = (
        "is_active",
        "opens_in_new_tab",
        "order",
    )

    search_fields = (
        "label",
        "url",
    )

    ordering = (
        "order",
        "label",
    )
