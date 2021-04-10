from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
	path('', views.analysis, name = 'analyticshome'),
    path('analysis/', views.analysis, name = 'analytics'),
    path('analyseDaysTrend/', views.daysTrend, name = 'daysTrend'),
    path('priceTrend/', views.priceTrend, name = 'priceTrend'),
    
]
