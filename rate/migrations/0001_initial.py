# Generated by Django 5.0.6 on 2024-05-14 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('metrices', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('pub_date', models.DateField()),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrices.metrices')),
                ('rated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated', to=settings.AUTH_USER_MODEL)),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]