# Generated by Django 5.0.1 on 2024-01-27 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='user_id',
            new_name='user',
        ),
    ]
