"""
URL configuration for application project.

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
from django.urls import path, re_path
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.views.generic import TemplateView
from django.views import static
from apps.system.views import fetch_graph, fetch_cardList, fetch_wordCloud, fetch_emotionData, fetch_chartData, fetch_topicCard, fetch_event


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API Documentation for HotSpot Analyzer System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.user.urls")),
    path("api/", include("apps.dashboard.urls")),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^static/(?P<path>.*)$',static.serve,{'document_root':settings.STATIC_ROOT}, name='static'),
    path('fetch-graph/', fetch_graph, name='fetch-graph'),
    path('fetch-cardList/', fetch_cardList, name='fetch-cardList'),
    path('fetch-wordCloud/', fetch_wordCloud, name='fetch-wordCloud'),
    path('fetch-emotionData', fetch_emotionData, name='fetch-emotionData'),
    path('fetch-chartData', fetch_chartData, name='fetch-chartData'),
    path('fetch-topicCard', fetch_topicCard, name='fetch-topicCard'),
    path('fetch-event', fetch_event, name='fetch-event')
]