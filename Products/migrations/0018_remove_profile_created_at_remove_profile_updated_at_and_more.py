# Generated by Django 5.1.5 on 2025-02-14 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0017_profile_created_at_profile_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
