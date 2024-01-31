from django.db import models

# Create your models here.

class Course(models.Model):
    owner=models.CharField(max_length=50)
    course_name=models.CharField(max_length=50)
    price=models.FloatField(null=True)
    final_rating=models.DecimalField(decimal_places=1, max_digits=2, null=True)
    link=models.TextField(null=True)
    pub_date=models.DateField(null=True)

class User(models.Model):
    last_name=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    patronymic=models.TextField(null=True)
    email=models.EmailField()
    password=models.CharField(max_length=80)

class Review(models.Model):
    text_review=models.TextField(null=True)
    rating=models.IntegerField(null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

class Favorite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

