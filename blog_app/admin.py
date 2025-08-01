from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'icon_tag')
    list_filter = ('status',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'short_description')
    inlines = [ServiceFeatureInline]
    readonly_fields = ['icon_tag', 'preview_main_image']

    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'short_description', 'description',
                'status'
            )
        }),
        ("Images", {
            'fields': (
                'icon_image',
                'icon_tag',
                'main_image',
                'preview_main_image',
            )
        }),
    )

    def preview_main_image(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; height: auto; border:1px solid #ddd;" />',
                obj.main_image.url
            )
        return "-"
    preview_main_image.short_description = "Main Image Preview"

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'service')
    search_fields = ('title', 'short_description')


#    blog post admin

# فرم سفارشی با CKEditor
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="Full Content")

    class Meta:
        model = BlogPost
        fields = '__all__'


# پنل مدیریت سفارشی
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm

    list_display = ('title', 'category','status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at','category')
    list_editable = ('status',)
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)                                                                     
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status')
        }),
        ("Images", {
            'fields': ('thumbnail', 'main_image')
        }),
        ("Content", {
            'fields': ('summary', 'content')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )
