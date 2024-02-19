from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Course(models.Model):
    owner=models.CharField(max_length=50)
    course_name=models.CharField(max_length=150)
    price=models.FloatField(null=True)
    final_rating=models.DecimalField(decimal_places=1, max_digits=2, null=True, verbose_name='Рейтинг курса')
    link=models.TextField(null=True)
    training_period=models.IntegerField(null=True)

    def __str__(self):
        return self.course_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    patronymic=models.TextField(null=True)
    email=models.EmailField()
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Review(models.Model):
    text_review=models.TextField(default='')
    rating=models.DecimalField(decimal_places=1, max_digits=2, null=True, verbose_name='Рейтинг человека')
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_review

class Favorite(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.course}'

