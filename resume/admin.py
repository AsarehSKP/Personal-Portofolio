from django.contrib import admin
from .models import Project


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

