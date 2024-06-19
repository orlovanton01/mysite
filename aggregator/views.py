from django.shortcuts import render, redirect
from rest_framework import routers, serializers, viewsets
import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

from django.contrib.auth.models import User
from .models import Course, Favorite, Сomparison, Review #, Profile
import csv

from rest_framework import serializers    
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.db import migrations
from django.contrib.postgres import operations
from rest_fuzzysearch import search
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from rest_framework.settings import api_settings
from django.utils.translation import gettext_lazy as _

class TrigramSimilaritySearchFilter(SearchFilter):
    search_param = api_settings.SEARCH_PARAM
    template = 'rest_framework/filters/search.html'
    search_title = _('Search')
    search_description = _('A search term.')

    def get_trigram_similarity(self, view, request):
        return getattr(view, 'trigram_similarity', 0.3)

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()

    def get_search_fields(self, view, request):
        """
        Search fields are obtained from the view, but the request is always
        passed to this method. Sub-classes can override this method to
        dynamically change the search fields based on request content.
        """
        return getattr(view, 'search_fields', None)

    def filter_queryset(self, request, queryset, view):
        trigram_similarity = self.get_trigram_similarity(view, request)
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        # if no search_terms return
        if not search_terms:
            return queryset

        # make conditions
        conditions = []
        for search_term in search_terms:
            conditions.extend([
                TrigramSimilarity(field, search_term) for field in search_fields
        ])

        # take the greatest similarity from all conditions
        # and annotate as similarity
        return queryset.annotate(
            similarity=Greatest(*conditions)
        ).filter(similarity__gte=trigram_similarity)


class CourseFilter(django_filters.FilterSet):
    #search = filters.CharFilter(field_name="course_name", lookup_expr="contains")
    search = search.RankedFuzzySearchFilter()
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_training_period = filters.NumberFilter(field_name="training_period", lookup_expr='gte')
    max_training_period = filters.NumberFilter(field_name="training_period", lookup_expr='lte')
    class Meta:
        model = Course
        fields = '__all__'
        exclude ="owner_img"

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        operations.TrigramExtension(),
    ]

class CourseSerializer(serializers.ModelSerializer):
    get_course_img_url = serializers.CharField(read_only=True)
    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ("owner_img",)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend, search.RankedFuzzySearchFilter,)
    ordering_fields = '__all__'
    search_fields = ["course_name"]
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
    author = serializers.CharField(source='user.username', read_only=True)
    course = CourseSerializer()
    class Meta:
        model = Review
        fields = ['id', 'course', 'text_review', 'user', 'author',]
    
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