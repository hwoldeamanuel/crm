from django.urls import path, include

from . import views



urlpatterns = [
   
   
    path('', views.partnership, name='partnership'),
    path('profile/<int:id>/', views.partnership_profile, name='pprofile'),
]