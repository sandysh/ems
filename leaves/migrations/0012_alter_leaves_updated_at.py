# Generated by Django 5.0.6 on 2025-01-28 06:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leaves", "0011_alter_leaves_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaves",
            name="updated_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
