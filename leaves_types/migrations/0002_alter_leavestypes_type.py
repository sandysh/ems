# Generated by Django 5.0.6 on 2024-10-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves_types', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavestypes',
            name='type',
            field=models.CharField(max_length=250),
        ),
    ]