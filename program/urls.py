from django.urls import path, include

from . import views



urlpatterns = [
   
    path('', views.program_list, name='programs'),
    path('program/', views.program_list, name='programs'),
    path('new/', views.program_add, name='add_program'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('program/edit/<int:id>/', views.program_edit, name='edit_program'),
    
]

htmxpatterns = [
    path('program_filter/', views.program_list_filter, name='program_filter'),

    path('program_profile/<int:id>/', views.program_profile, name='program_profile'),
    path('edit_program_profile/<int:id>/', views.program_profile_edit, name='edit_program_profile'),
    

    path('users/<int:id>/', views.user_list, name='user_list'),
    path('tusers/<int:id>/', views.user_travel_list, name='user_travel_list'),
    path('partnership/<int:id>/', views.program_partnership, name='partnership_list'),
    path('user_add/<int:id>/', views.add_user, name='add_user'),
    path('add_travel_user/<int:id>/', views.add_travel_user, name='add_travel_user'),
    path('edit_user_roles/<int:uid>/', views.edit_user_role, name='edit_user_role'),


    path('region/<int:id>/', views.region, name='region'),  
    path('region/zones/', views.zones, name='zones'),
    path('region/zones/woredas/', views.woredas, name='woredas'),
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),
    
 
   
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),

    path('area/<str:pk>/edit/', views.area_edit_form, name='area_edit_form'),
   
 
    
   
    path('indicators/<int:id>/', views.indicator_list, name='indicator_list'),
    path('indicator_add/<int:id>/', views.add_indicator, name='add_indicator'),
    path('partnership_add/<int:id>/', views.add_partnership, name='add_partnership'),
    path('indicator/<int:pk>/remove', views.remove_indicator, name='remove_indicator'),
    path('indicator/<int:pk>/edit', views.edit_indicator, name='edit_indicator'),
    path('parnership/<int:pk>/edit', views.edit_partnership, name='edit_partnership'),
    
    path('area_list/<int:id>/', views.area_list, name='area_list'),
    path('region/edit_area/<int:pk>/', views.area_edit_form, name='area_edit_form'),
    path('update_user_roles/<int:id>/', views.update_user_roles, name='update_user_roles'),
    path('update_travel_user_roles/<int:id>/', views.update_travel_user_roles, name='update_travel_user_roles'),
   
    path('remove_user_role/<int:pk>/', views.remove_user_role, name='remove_user_role'),
    path('newportfolio/', views.newportfolio, name='newportfolio'),
     path('remove_travel_user_role/<int:pk>/', views.remove_travel_user_role, name='remove_travel_user_role'),
   

   
]
 


urlpatterns += htmxpatterns