# Generated by Django 5.1.5 on 2025-01-28 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0002_alter_platform_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='logo',
            field=models.ImageField(blank=True, default='logos/default.jpg', null=True, upload_to='logos'),
        ),
    ]
