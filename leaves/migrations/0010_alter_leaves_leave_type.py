# Generated by Django 5.0.6 on 2024-10-30 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0009_alter_leaves_leave_type_alter_leaves_status'),
        ('leaves_types', '0002_alter_leavestypes_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='leaves_types.leavestypes'),
        ),
    ]