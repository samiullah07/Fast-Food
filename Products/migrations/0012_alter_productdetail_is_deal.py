# Generated by Django 5.1.5 on 2025-02-07 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0011_alter_productdetail_is_deal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='is_deal',
            field=models.BooleanField(default=False),
        ),
    ]
