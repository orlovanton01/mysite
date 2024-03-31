# Generated by Django 5.0.1 on 2024-03-26 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0023_remove_favorite_course_favorite_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='course',
        ),
        migrations.AddField(
            model_name='favorite',
            name='course',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='aggregator.course'),
            preserve_default=False,
        ),
    ]
