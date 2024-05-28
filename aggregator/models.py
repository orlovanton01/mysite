from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from os import path
from django.conf import settings

# Create your models here.

class Course(models.Model):
    owner=models.CharField(max_length=50)
    owner_img=models.ImageField(default='default.png')
    course_name=models.CharField(max_length=150)
    price=models.DecimalField(decimal_places=2, max_digits=8, default=0)
    final_rating=models.DecimalField(decimal_places=1, max_digits=2, null=True, verbose_name='Рейтинг курса')
    link=models.TextField(default='')
    training_period=models.IntegerField(default=0)

    def __str__(self):
        return self.course_name
    
    def get_course_img_url(self):
        file_name = self.owner + '.png'
        if path.exists(path.join(settings.MEDIA_ROOT, file_name)):
            self.owner_img.name = file_name
        else:
            self.owner_img.name = 'default.png'
        return self.owner_img.url

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     last_name=models.CharField(max_length=50)
#     first_name=models.CharField(max_length=50)
#     patronymic=models.TextField(null=True)
#     email=models.EmailField()
    
#     def __str__(self):
#         return f'{self.last_name} {self.first_name} {self.patronymic}'
    
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         try:
#             instance.profile.save()
#         except ObjectDoesNotExist:
#             Profile.objects.create(user=instance)
#         if created:
#             Profile.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()

class Review(models.Model):
    text_review=models.TextField(default='')
    rating=models.DecimalField(decimal_places=1, max_digits=2, null=True, verbose_name='Рейтинг человека')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_review


class Favorite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    # course=models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.user} {self.course}'
    
class Сomparison(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    # course=models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.user} {self.course}'
         
    
