from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from .data import search_amount, total_items, total_blogs

@api_view(['GET'])
def apiOverview(request):
  api_urls = {
      'blogKeyword': '/blog-keyword',
      'sellerKeyword': '/seller-keyword',
      
  }
  return Response(api_urls)

@api_view(['POST'])
def blog_keyword(request):  
  print(request.data["keyword"])
  pc_mobile_serach = search_amount(request.data["keyword"])
  total_item = total_items(request.data["keyword"])
  api = {
      "pc_serach": pc_mobile_serach["pc_serach"],
  "mobile_serach": pc_mobile_serach["mobile_serach"],
  "total_itme": total_item
  }
  return Response(api)

@api_view(['POST'])
def seller_keyword(request):
  print(request.data["keyword"])   
  pc_mobile_serach = search_amount(request.data["keyword"])
  total_blog = total_blogs(request.data["keyword"])
  api = {
      "pc_serach": pc_mobile_serach["pc_serach"],
  "mobile_serach": pc_mobile_serach["mobile_serach"],
  "total_blogs_daum": total_blog["daum"],
  "total_blogs_naver": total_blog["naver"]
  }
  return Response(api)
