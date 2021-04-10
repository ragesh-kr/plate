"""plate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from home import views as home_views
from analytics import views as analytics_view
from birdview import views as bview
from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',bview.dashboard, name='birdview'),
    path('',include('home.urls')),
    path('dashboard/', home_views.dashboard, name='dashboard'),
    path('analytics/', include('analytics.urls')),
    path('dashboard/test/',home_views.test,name='test'),
    path('test/',home_views.test,name='test'),
    path('itemsAjax/',home_views.itemsAjax,name='itemsAjax'),
    path('dashboard/itemsAjax/',home_views.itemsAjax,name='itemsAjax'),
    path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    
]
