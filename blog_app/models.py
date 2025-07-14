from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from PIL import Image
from ckeditor.fields import RichTextField
from django.urls import reverse


#  ServiceQuerySet   and    manager
class ServiceQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Service.Status.PUBLISHED)

class ServiceManager(models.Manager):
    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Service(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField("Title", max_length=100)
    short_description = models.CharField("Short Description", max_length=200, blank=True)
    description = models.TextField("Description", blank=True)

    icon_image = models.ImageField("Service Icon (For Card)", upload_to='services/icons/', blank=True, null=True)
    main_image = models.ImageField("Main Image (For Details Page)", upload_to='services/images/', blank=True, null=True)

    slug = models.SlugField("Slug", unique=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    order = models.PositiveIntegerField("Display Order", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    all_objects = models.Manager()
    objects = ServiceManager()

    MAIN_IMAGE_SIZE = (800, 450)  # لنداسکیپ
    # ICON_IMAGE_SIZE = (300, 300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        # resize icon image if exists
        if self.icon_image:
            try:
                img = Image.open(self.icon_image.path)
                img = img.convert("RGB")
                img.thumbnail(self.ICON_IMAGE_SIZE)
                img.save(self.icon_image.path, quality=90)
            except Exception as e:
                print(f"Icon image resize error: {e}")

        # crop and resize main image to landscape
        if self.main_image:
            try:
                img = Image.open(self.main_image.path)
                img = img.convert("RGB")
                img = self.crop_to_landscape(img, self.MAIN_IMAGE_SIZE)
                img.save(self.main_image.path, quality=90)
            except Exception as e:
                print(f"Main image crop error: {e}")

    def crop_to_landscape(self, img, target_size):
        target_w, target_h = target_size
        original_w, original_h = img.size
        target_ratio = target_w / target_h
        original_ratio = original_w / original_h

        if original_ratio > target_ratio:
            # برش افقی از وسط
            new_width = int(original_h * target_ratio)
            left = (original_w - new_width) // 2
            right = left + new_width
            top = 0
            bottom = original_h
        else:
            # برش عمودی از وسط
            new_height = int(original_w / target_ratio)
            top = (original_h - new_height) // 2
            bottom = top + new_height
            left = 0
            right = original_w

        img = img.crop((left, top, right, bottom))
        img = img.resize(target_size, Image.ANTIALIAS)
        return img

    def icon_tag(self):
        if self.icon_image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: contain;" />',
                self.icon_image.url
            )
        return "-"
    icon_tag.short_description = 'Icon'

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="features")
    title = models.CharField("Feature Title", max_length=100)
    short_description = models.CharField("Short Description", max_length=200, blank=True)

    class Meta:
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features"

    def __str__(self):
        return self.title


#   Blog Queryset manager

class BlogQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=BlogPost.Status.PUBLISHED)


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class BlogPost(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    summary = models.TextField("Summary", blank=True)
    content = RichTextField("Full Content", blank=True)

    thumbnail = models.ImageField("Thumbnail Image", upload_to='blog/thumbnails/', blank=True, null=True)
    main_image = models.ImageField("Main Article Image", upload_to='blog/main_images/', blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_name = models.CharField("Author Name", max_length=100, blank=True)
    author_bio = models.TextField("Author Bio", blank=True)
    author_image = models.ImageField("Author Image", upload_to='authors/', blank=True, null=True)

    objects = BlogManager()
    all_objects = models.Manager()

    THUMBNAIL_SIZE = (600, 400)
    MAIN_IMAGE_SIZE = (1200, 800)



    def get_absolute_url(self):
        return reverse('blog_app:blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Resize images after save
        self.resize_image(self.thumbnail, self.THUMBNAIL_SIZE)
        self.resize_image(self.main_image, self.MAIN_IMAGE_SIZE)

    def resize_image(self, image_field, size):
        if image_field:
            try:
                img = Image.open(image_field.path)
                img.thumbnail(size)
                img.save(image_field.path)
            except Exception as e:
                print(f"Image resize error: {e}")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

