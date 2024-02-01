from django.shortcuts import get_object_or_404, render

from .models import Course

def index(request):
    latest_courses_list=Course.objects.all()
    context = {"latest_courses_list": latest_courses_list}
    return render(request, "aggregator/index.html", context)

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "aggregator/detail.html", {"course": course})