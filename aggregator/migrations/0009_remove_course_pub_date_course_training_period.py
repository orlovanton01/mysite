# Generated by Django 5.0.1 on 2024-02-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0008_alter_course_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='course',
            name='training_period',
            field=models.DurationField(null=True),
        ),
    ]
