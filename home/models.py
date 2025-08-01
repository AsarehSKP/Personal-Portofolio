from django.db import models
from django.utils.text import slugify


class About(models.Model):
    full_name = models.CharField("Full Name", max_length=100)
    role = models.CharField("Professional Role", max_length=100, help_text="e.g. Backend Developer")
    bio = models.TextField("Biography")
    experience = models.PositiveIntegerField("Experience", default=1)
    based_in = models.CharField("Based In", max_length=50, help_text="e.g. Remote / Germany")
    availability = models.CharField("Availability", max_length=50, help_text="e.g. Freelance / Full-time")

    email = models.EmailField("Email")
    linkedin_url = models.URLField("LinkedIn", blank=True, null=True)
    github_url = models.URLField("GitHub", blank=True, null=True)

    profile_image = models.ImageField("Profile Image", upload_to="profile/", blank=True, null=True)
    cv_file = models.FileField("CV File", upload_to="cv/", blank=True, null=True)

    project_count = models.PositiveIntegerField("Completed Projects", default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# PROFILE

class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_pictures')
    cv_file = models.FileField(upload_to='cv_files', blank=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.full_name


class Contact(models.Model):
    name = models.CharField("Name", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Subject", max_length=100)
    message = models.TextField("Message")

    is_read = models.BooleanField("Read", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(help_text="from 1 to 100")

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Site_info(models.Model):
    address = models.CharField("Address", max_length=250, blank=True, null=True)
    email = models.EmailField("Email")
    linkedin_url = models.URLField("LinkedIn", blank=True, null=True)
    github_url = models.URLField("GitHub", blank=True, null=True)

    def __str__(self):
        return f"{self.address} - {self.email}"

    class Meta:
        verbose_name = 'Site Info'
        verbose_name_plural = 'Site Infos'


class Category(models.Model):
    title = models.CharField("Title", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True, )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', kwargs={'slug': self.slug})
