from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import os
from django.conf import settings


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField("Project Title", max_length=200)
    slug = models.SlugField("Slug", unique=True, blank=True)

    short_description = models.TextField("Short Description", blank=True)
    description = RichTextField("Full Description")  # ویرایشگر حرفه‌ای CKEditor

    tech_stack = models.CharField(
        "Technologies Used",
        max_length=255,
        help_text="e.g. Django, React, PostgreSQL"
    )

    project_type = models.CharField(
        "Project Type",
        max_length=100,
        help_text="e.g. Web App, API, Automation"
    )

    main_image = models.ImageField("Main Image", upload_to='projects/images/')

    source_code_url = models.URLField("Source Code (GitHub)", blank=True, null=True)
    live_demo_url = models.URLField("Live Demo URL", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    MAIN_IMAGE_SIZE = (1200, 800)  # هدف برای resize تصویر

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        self.resize_image(self.main_image, self.MAIN_IMAGE_SIZE)

    def resize_image(self, image_field, size):
        if image_field and os.path.isfile(image_field.path):
            try:
                img = Image.open(image_field.path)
                img = img.convert("RGB")  # برای جلوگیری از خطاهای RGBA
                img.thumbnail(size, Image.ANTIALIAS)
                img.save(image_field.path)
            except Exception as e:
                print(f"Error resizing image: {e}")

    def get_absolute_url(self):
        return reverse('resume:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"