from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import routers, serializers, viewsets
import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Course
import csv

class CourseFilter(django_filters.FilterSet):
    search = filters.CharFilter(field_name="course_name", lookup_expr="icontains")
    class Meta:
        model = Course
        fields = '__all__'
        exclude ="owner_img"

class CourseSerializer(serializers.ModelSerializer):
    get_course_img_url = serializers.CharField(read_only=True)
    class Meta:
        model = Course
        fields = "__all__"

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = '__all__'
    filterset_class = CourseFilter

def index(request):
    latest_courses_list=Course.objects.order_by("course_name")
    context = {"latest_courses_list": latest_courses_list}
    return render(request, "aggregator/index.html", context)


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "aggregator/detail.html", {"course": course})
