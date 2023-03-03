"""financeHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from assetManager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home_page'),
    path('connect_investments/', views.connect_investments, name='connect_investments'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('api/number/', views.number_view, name='number'),
    path('monthly_graphs/', views.monthlyGraph, name='monthlyGraph'),
    path('weekly_graphs/', views.weeklyGraph, name='weeklyGraph'),
    path('api/investment_categories/', views.investment_categories, name='investment_categories'),
    path('api/investment_category_breakdown/', views.investment_category_breakdown, name='investment_category_breakdown')
]
