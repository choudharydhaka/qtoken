"""qtoken URL Configuration

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
from django.urls import path


from . import views
app_name = 'liquor'
urlpatterns = [
    path('', views.index, name='index'),
  #  path('register', views.register, name='register'),    
    #path('index', views.register, name='index'),
    #path('', views.index, name='index'),
     # ex: /polls/5/
    path('search', views.searchStore, name='search'),
    path('stores', views.stores, name='stores'),     

    #path('stores/register', views.stores, name='storeRegister'),  
    path('stores/<str:store_id>/', views.tokens,{'day': None}, name='tokens'),
    path('stores/<str:store_id>/<str:day>', views.tokens, name='tokens'),
   # path('stores/<str:store_id>/today', views.tokens, {"day":"today"},name='tokens'), 
]