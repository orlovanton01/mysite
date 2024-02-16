from django.db import models

# Create your models here.

class Course(models.Model):
    owner=models.CharField(max_length=50)
    course_name=models.CharField(max_length=50)
    price=models.DecimalField(decimal_places=2, max_digits=8, default=0)
    final_rating=models.DecimalField(decimal_places=1, max_digits=2, null=True, verbose_name='Рейтинг курса')
    link=models.TextField(default='')
    training_period=models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

class User(models.Model):
    last_name=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    patronymic=models.TextField(null=True)
    email=models.EmailField()
    password=models.CharField(max_length=80)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

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

    def __str__(self):
        return f'{self.user} {self.course}'

