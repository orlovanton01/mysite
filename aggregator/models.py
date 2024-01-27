from django.db import models

# Create your models here.

class Course(models.Model):
    owner=models.CharField(max_length=50)
    course_name=models.CharField(max_length=50)
    price=models.FloatField
    final_rating=models.DecimalField(decimal_places=1, max_digits=2)
    link=models.TextField

class User(models.Model):
    last_name=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    patronymic=models.TextField
    email=models.CharField(max_length=80)
    password=models.CharField(max_length=80)

class Review(models.Model):
    text_review=models.TextField
    rating=models.IntegerField
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

class Favorite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

