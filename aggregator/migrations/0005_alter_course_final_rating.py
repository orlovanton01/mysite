# Generated by Django 5.0.1 on 2024-01-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0004_rename_course_id_favorite_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='final_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]