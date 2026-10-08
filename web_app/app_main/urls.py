
from django.contrib import admin
from django.urls import path
from app_main import views

urlpatterns = [
    path('resume/<int:id>/', views.resume,name='resume'),
    path('', views.index,name='index'),
    path('resume/edit', views.resume_edit,name='resume_edit'),
]
