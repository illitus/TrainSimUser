from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select, name='select' ),
    path('results',views.schedule,name='schedule'),
    path('<slug:routecode>',views.route_info,name='route_info'),
]