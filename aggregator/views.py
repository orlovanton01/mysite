from django.shortcuts import render, redirect
from rest_framework import routers, serializers, viewsets
import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from django.contrib.auth.models import User
from .models import Course, Favorite, Сomparison, Review #, Profile
import csv

from rest_framework import serializers    
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CourseFilter(django_filters.FilterSet):
    search = filters.CharFilter(field_name="course_name", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_training_period = filters.NumberFilter(field_name="training_period", lookup_expr='gte')
    max_training_period = filters.NumberFilter(field_name="training_period", lookup_expr='lte')
    class Meta:
        model = Course
        fields = '__all__'
        exclude ="owner_img"

class CourseSerializer(serializers.ModelSerializer):
    get_course_img_url = serializers.CharField(read_only=True)
    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ("owner_img",)

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


class FavSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Favorite
        fields = "__all__"
    
class FavSerializerPost(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    user= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Favorite
        fields = "__all__"

    def create(self, validated_data):
        instance, _ = Favorite.objects.get_or_create(**validated_data)
        return instance

class FavFilter(django_filters.FilterSet):
    class Meta:
        model = Favorite
        fields = ['user']

class FavViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FavFilter
    ordering_fields = '__all__'

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return FavSerializer
        else:
            return FavSerializerPost
        

class ComSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Сomparison
        fields = "__all__"
    
class ComSerializerPost(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    user= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Сomparison
        fields = "__all__"

    def create(self, validated_data):
        instance, _ = Сomparison.objects.get_or_create(**validated_data)
        return instance

class ComFilter(django_filters.FilterSet):
    class Meta:
        model = Сomparison
        fields = ['user']

class ComViewSet(viewsets.ModelViewSet):
    queryset = Сomparison.objects.all()
    serializer_class = ComSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ComFilter
    ordering_fields = '__all__'

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return ComSerializer
        else:
            return ComSerializerPost
        

class RevSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Review
        fields = "__all__"
    
class RevSerializerPost(WritableNestedModelSerializer, serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    user= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        instance, _ = Review.objects.get_or_create(**validated_data)
        return instance

class RevFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = ['user', 'course']

class RevViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = RevSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RevFilter
    ordering_fields = '__all__'

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return RevSerializer
        else:
            return RevSerializerPost