# Generated by Django 5.0.6 on 2024-05-16 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_alter_leaves_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='leave_type',
            field=models.CharField(choices=[('CASUAL', 'casual'), ('SICK', 'sick')]),
        ),
    ]
