from django.shortcuts import render

from .models import Course

def index(request):
    latest_courses_list=Course.objects.all()
    context = {"latest_courses_list": latest_courses_list}
    return render(request, "aggregator/index.html", context)