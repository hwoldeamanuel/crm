
from django.urls import path, include

from django.contrib.auth.views import LogoutView
from . import views


from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name='home'),
   
   
    
    path('dashboard/', views.dashboard_fleet, name='dashboard'),
    path('program_activity/', views.program_activity, name='program_activity'),
    path('get_date/', views.get_date, name='get_date'),
    
    
]
  
  

