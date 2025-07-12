from django.urls import path, include

from . import views



urlpatterns = [
   
    path('', views.user_setting, name='user_setting'),
    path('account/', views.user_setting, name='user_setting'),
    path('boundaries/', views.admin_boundary, name='admin_boundary'),
    path('project_types/', views.project_type, name='project_type'),
    path('users_list/', views.users_list, name='users_list'),
    path('users_filter/', views.users_filter, name='users_filter'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('admin_list/', views.admin_list, name='admin_list'),
    path('admin_filter/', views.admin_filter, name='admin_filter'),
    path('edit_woreda/<int:id>/', views.edit_woreda, name='edit_woreda'),
    path('edit_zone/<int:id>/', views.edit_zone, name='edit_zone'),
    path('edit_region/<int:id>/', views.edit_region, name='edit_region'),
    path('add_woreda/', views.add_woreda, name='add_woreda'),
    path('add_region/', views.add_region, name='add_region'),
    path('add_zone/', views.add_zone, name='add_zone'),
    path('type_list/', views.type_list, name='type_list'),
    
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('edit_type/<int:id>/', views.edit_type, name='edit_type'),
    path('add_type/', views.add_type, name='add_type'),
    path('add_category/', views.add_category, name='add_category'),
    path('type_filter/', views.type_filter, name='type_filter'),
    path('account/<int:id>/', views.user_detail, name='user_detail'),
    path('account/profile/<int:id>/', views.user_detail_profile, name='user_detail_profile'),
    path('group/<int:id>/', views.user_group, name='user_group'),
    path('account_group_edit/<int:id>/', views.user_group_edit, name='user_group_edit'),
    path('group_edit/<int:id>/', views.group_edit, name='group_edit'),
    path('group_add/', views.add_group, name='add_group'),
    path('group_list/', views.group_list, name='group_list'),
    path('group_delete/<int:id>/', views.group_delete, name='group_delete'),
    path('groups/', views.group_setting, name='group_setting'),
    path('groups_filter/', views.groups_filter, name='groups_filter'),
    path('user_roles/<int:id>/', views.user_roles, name='user_roles'),
    path('update_user_program_roles/<int:id>/', views.update_user_program_roles, name='update_user_program_roles'),
    path('add_user_program_role/<int:id>/', views.add_user_program_role, name='add_user_program_role'),
    path('remove_user_program_role/<int:pk>/', views.remove_user_program_role, name='remove_user_program_role'),
    path('iworeda/', views.iworeda, name='iworeda'),

]