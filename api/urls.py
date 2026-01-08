from django.urls import path
from .views import *
# habtamu changes
urlpatterns = [
    path('region/', RegionList.as_view()),
    path('region/<int:pk>/', RegionDetail.as_view()),
    path('country/', CountryList.as_view()),
    path('country/<int:pk>/', CountryDetail.as_view()),
    path('zone/', ZoneList.as_view()),
    path('zone/<int:pk>/', ZoneDetail.as_view()),
    path('woreda/', WoredaList.as_view()),
    path('woreda/<int:pk>/', WoredaDetail.as_view()),
    path('icn/', IcnList.as_view()),
    path('activity/', ActivityList.as_view()),


]