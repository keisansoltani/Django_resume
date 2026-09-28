
from django.contrib import admin
from django.urls import path
from app_main import views

urlpatterns = [
    path('resume/<int:id>/', views.resume),
    path('', views.index),
]
