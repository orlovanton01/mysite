# Generated by Django 5.0.1 on 2024-03-23 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0020_alter_course_owner_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='owner_img',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
