from django.contrib import admin

# Register your models here.

from .models import Course, Profile, Review, Favorite

admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Favorite)