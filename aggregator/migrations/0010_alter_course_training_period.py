# Generated by Django 5.0.1 on 2024-02-01 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0009_remove_course_pub_date_course_training_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='training_period',
            field=models.IntegerField(null=True),
        ),
    ]
