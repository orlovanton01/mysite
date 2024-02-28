from django.shortcuts import get_object_or_404, render, redirect

from .models import Course
import csv

def index(request):
    latest_courses_list=Course.objects.order_by("course_name")
    context = {"latest_courses_list": latest_courses_list}
    return render(request, "aggregator/index.html", context)

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "aggregator/detail.html", {"course": course})
