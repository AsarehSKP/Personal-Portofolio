from django.contrib import admin
from home.models import *
from resume.models import Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'title')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id','name' ,'percentage')

# Register your models here.


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'experience', 'based_in', 'availability', 'project_count')
    search_fields = ('full_name', 'role', 'email')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_per_page = 20

    def has_add_permission(self, request):
        # جلوگیری از اضافه کردن پیام جدید از پنل ادمین
        return False

@admin.register(Site_info)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['address', 'email', 'linkedin_url', 'github_url']
    search_fields = ('address', 'email', 'linkedin_url', 'github_url')


