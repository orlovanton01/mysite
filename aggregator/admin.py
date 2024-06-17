from django.contrib import admin


# Register your models here.

from .models import Course, Review, Favorite, Сomparison, Review #, Profile
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

class CourseAdmin(ImportExportModelAdmin):
    resouce_classes = [CourseResource]


admin.site.register(Course, CourseAdmin)
# admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Сomparison)