# Generated by Django 5.2.1 on 2025-06-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author_bio',
            field=models.TextField(blank=True, verbose_name='Author Bio'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='author_image',
            field=models.ImageField(blank=True, null=True, upload_to='authors/', verbose_name='Author Image'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='author_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Author Name'),
        ),
    ]
