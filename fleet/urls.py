

from django.urls import path, include

from . import views


urlpatterns = [
   
    path('', views.fleets, name='fleets'),
    path('fleets/', views.fleets, name='fleets'),
    
    path('fleet_list/', views.fleet_list, name='fleet_list'),
    path('fleets/<int:id>/', views.fleet, name='fleet'),
    path('fleet_profile/<int:id>/', views.fleet_profile, name='fleet_profile'),
    path('edit_fleet/<int:id>/', views.edit_fleet, name='edit_fleet'),
    path('edit_fleet_log/<int:fid>/<int:id>/', views.edit_fleet_log, name='edit_fleet_log'),
    path('fleet/add/', views.add_fleet, name='add_fleet'),
    path('fleet_filter/', views.fleet_filter, name='fleet_filter'),
    path('fleet_log/add/<int:id>/', views.add_fleet_log, name='add_fleet_log'),
    path('download_log_sheet/<int:id>/', views.download_logsheet, name='download_logsheet'),
    path('generators/', views.generators, name='generators'),
    path('partial_fleet_log/<int:id>/', views.partial_fleet_log, name='partial_fleet_log'),
    path('removefleetlog/<int:pk>/', views.remove_fleetlog, name='remove_fleetlog'),
    path('fleet_activity/<int:id>/', views.fleet_activity, name='fleet_activity'),
    path('download_gen_log_sheet/<int:id>/', views.download_gen_logsheet, name='download_gen_logsheet'),
    path('edit_fleet_expense/<int:fid>/<int:id>/', views.edit_fleet_expense, name='edit_fleet_expense'),
    path('partial_fleet_expense/<int:id>/', views.partial_fleet_expense, name='partial_fleet_expense'),
    path('removefleetexpense/<int:pk>/', views.remove_fleetexpense, name='remove_fleetexpense'),
    path('fleet_expense/add/<int:id>/', views.add_fleet_expense, name='add_fleet_expense'),
    path('generators/', views.generators, name='generators'),
    path('generators/generator/<int:id>/', views.generator, name='generator'),
    path('generator_activity/<int:id>/', views.generator_activity, name='generator_activity'),
    path('edit_generator/<int:id>/', views.edit_generator, name='edit_generator'),
    path('edit_generator_report/<int:fid>/<int:id>/', views.edit_generator_report, name='edit_generator_report'),
    path('generator_report/add/<int:id>/', views.add_generator_report, name='add_generator_report'),
    path('partial_generator_report/<int:id>/', views.partial_generator_report, name='partial_generator_report'),
    path('remove_generator_report/<int:pk>/', views.remove_generator_report, name='remove_generator_report'),
    path('generator_profiley/<int:id>/', views.generator_profile, name='generator_profile'),
    
    path('reports/', views.missing_report, name='report'),
    
    path('missing_report/', views.missing_report, name='missing_report'),
    path('aggregate_report/', views.aggregate_report, name='aggregate_report'),
  
    path('generate_report/', views.generate_report, name='generate_report'),
    path('years/', views.years, name='years'),
    path('get_report_form/', views.get_report_form, name='get_report_form'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),


]