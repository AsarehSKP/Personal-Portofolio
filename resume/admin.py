from django.contrib import admin
from .models import *



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'status', 'created_at')
    list_filter = ('status', 'project_type', 'created_at')
    search_fields = ('title', 'description', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'project_type', 'status')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Links', {
            'fields': ('source_code_url', 'live_demo_url')
        }),
        ('Metadata', {
            'fields': ('tech_stack', 'created_at', 'updated_at')
        }),
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'daterange', 'column', 'created_at']
    list_editable = ('column',)
    list_filter = ('column', 'created_at')
    search_fields = ('title', 'institution', 'daterange')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('daterange', 'title', 'institution', 'description', 'column')
        }),

    )


@admin.register(CV_pdf)
class CVPDFAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'updated_at', 'created_at')
    list_filter = ('first_name', 'last_name', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name')
    ordering = ('-updated_at',)

