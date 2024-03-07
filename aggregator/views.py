from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import routers, serializers, viewsets
import django_filters
from django_filters import rest_framework as filters

from .models import Course
import csv

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = '__all__'
        exclude ="owner_img"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseFilter

def index(request):
    latest_courses_list=Course.objects.order_by("course_name")
    context = {"latest_courses_list": latest_courses_list}
    return render(request, "aggregator/index.html", context)


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "aggregator/detail.html", {"course": course})
