from django.urls import path
from . import views
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('blog-keyword/', views.blog_keyword, name="blog_keyword"),
    path('seller-keyword/', views.seller_keyword, name="seller_keyword"),    
]