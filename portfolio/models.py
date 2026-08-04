from django.db import models
from django.core.validators import FileExtensionValidator


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=120)
    summary = models.TextField(max_length=250)

    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    cover_image = models.ImageField(
        upload_to="portfolio/projects/",
        blank=True,
        null=True,
    )

    desktop_image = models.ImageField(
        upload_to="portfolio/projects/",
        blank=True,
        null=True,
    )

    responsive_image = models.ImageField(
        upload_to="portfolio/projects/",
        blank=True,
        null=True,
    )

    live_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Optional live application URL shown on the project page.",
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Optional GitHub or source code URL shown on the project page.",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class CaseStudySection(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="case_study_sections",
    )

    order = models.PositiveIntegerField(default=1)

    section_number = models.CharField(
        max_length=10,
        blank=True,
    )

    eyebrow = models.CharField(
        max_length=120,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
    )

    introduction = models.TextField(
        blank=True,
    )

    large_image = models.ImageField(
        upload_to="portfolio/case_studies/",
        blank=True,
        null=True,
    )

    large_image_alt = models.CharField(
        max_length=255,
        blank=True,
    )

    large_image_caption = models.CharField(
        max_length=255,
        blank=True,
    )

    small_image = models.ImageField(
        upload_to="portfolio/case_studies/",
        blank=True,
        null=True,
    )

    small_image_alt = models.CharField(
        max_length=255,
        blank=True,
    )

    small_image_caption = models.CharField(
        max_length=255,
        blank=True,
    )

    closing_label = models.CharField(
        max_length=120,
        blank=True,
    )

    closing_text = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} — {self.section_number or self.order}: {self.title}"


class CaseStudyExpandable(models.Model):
    section = models.ForeignKey(
        CaseStudySection,
        on_delete=models.CASCADE,
        related_name="expandables",
    )

    order = models.PositiveIntegerField(default=1)

    number = models.CharField(
        max_length=10,
        blank=True,
        help_text="Optional. Leave empty for a standalone expandable.",
    )

    summary = models.CharField(
        max_length=255,
    )

    content = models.TextField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        prefix = f"{self.number} " if self.number else ""
        return f"{prefix}{self.summary}"


class ResumeDocument(models.Model):
    title = models.CharField(
        max_length=120,
        default="Ana Masiliuniene UX Resume",
    )

    file = models.FileField(
        upload_to="portfolio/resumes/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"],
            ),
        ],
    )

    is_active = models.BooleanField(
        default=True,
        help_text="The resume page uses the newest active upload.",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class AdditionalCertificate(models.Model):
    title = models.CharField(max_length=160)

    issuer = models.CharField(
        max_length=160,
        blank=True,
    )

    file = models.FileField(
        upload_to="portfolio/certificates/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"],
            ),
        ],
    )

    is_active = models.BooleanField(
        default=False,
        help_text="Enable this when the certificate should appear on the resume page.",
    )

    order = models.PositiveIntegerField(default=0)

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ContactLink(models.Model):
    label = models.CharField(max_length=80)

    url = models.CharField(
        max_length=500,
        help_text="Use a full URL, mailto: email link, or tel: phone link.",
    )

    opens_in_new_tab = models.BooleanField(
        default=True,
        help_text="Disable this for mailto: and tel: links.",
    )

    is_active = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label
