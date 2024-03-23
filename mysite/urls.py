"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from aggregator import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from aggregator.views import CourseViewSet
from rest_framework.authtoken import views
from . import loginhandler as lh

router = routers.DefaultRouter()

router.register(r'course', CourseViewSet)

# Это эндпоинты. К ним делаем запросы на порте 8000
urlpatterns = [
    path("", include("aggregator.urls")),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('token/', views.obtain_auth_token),

    path('csrf/', lh.get_csrf, name='api-csrf'),
    path('login/', lh.login_view, name='api-login'),
    path('logout/', lh.logout_view, name='api-logout'),
    path('session/', lh.session_view, name='api-session'),
    path('whoami/', lh.whoami_view, name='api-whoami'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)