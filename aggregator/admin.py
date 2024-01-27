from django.contrib import admin

# Register your models here.

from .models import Course, User, Review, Favorite

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Favorite)