from django.urls import path, include

from . import views




urlpatterns = [
   
    path('', views.icnreports, name='icnsreport'),
  
    path('intervention/', views.icnreports, name='icnsreport'),
    path('intervention/<int:id>/new/profile/', views.icnreport_add, name='icnreport_add'),
    path('intervention/<int:id>/profile/edit/', views.icnreport_edit, name='icnreport_edit'),
    path('intervention/<int:id>/impact/', views.icnreport_step_impact, name='icnreport_step_impact'),
    path('activity/<int:id>/impact/', views.activityreport_step_impact, name='activityreport_step_impact'),

    
    path('intervention/<int:id>/profile/', views.icnreport_detail, name='icnreport_detail'),
    path('intervention/<int:id>/approval/', views.icnreport_submit_approval, name='icnreport_submit_approval'),
    path('activity/<int:id>/approval/', views.activityreport_submit_approval, name='activityreport_submit_approval'),
    path('downloadi/<int:id>/', views.download, name='downloadi'),
    path('downloada/<int:id>/', views.downloada, name='downloada'),
    
    
   
   
   
    path('icnreport_submit_form_partial/<int:id>/', views.icnreport_submit_form_partial, name='icnreport_submit_form_partial'),
    path('activityreport_submit_form_partial/<int:id>/', views.activityreport_submit_form_partial, name='activityreport_submit_form_partial'),
    path('activity/', views.activitiesreport, name='activitiesreport'),
    path('activity/<int:id>/profile/', views.activityreport_detail, name='activityreport_detail'),
    path('activity/<int:id>/profile/add/', views.activityreport_add, name='activityreport_add'),
    path('activity/<int:id>/profile/edit/', views.activityreport_edit, name='activityreport_edit'),
   
    
]

htmxpatterns = [


 
 path('icnreport_submit_detail/<int:id>/', views.icnreport_submit_detail, name='icnreport_submit_detail'),
 path('icnreport_submit_list/<int:id>/', views.icnreport_submit_list, name='icnreport_submit_list'),


 path('icnreport_submit_form/<int:id>/<int:sid>/', views.icnreport_submit_form, name='icnreport_submit_form'),
 path('activityreport_submit_form/<int:id>/<int:sid>/', views.activityreport_submit_form, name='activityreport_submit_form'),
 path('icnreport_submit_document/<int:id>/', views.icnreport_submit_document, name='icnreport_submit_document'),
 path('activityreport_submit_document/<int:id>/', views.activityreport_submit_document, name='activityreport_submit_document'),
 path('icnreport_approvalp/<int:id>/<int:did>/', views.icnreport_approvalp, name='icnreport_approvalp'),
 path('icnreport_approvalf/<int:id>/<int:did>/', views.icnreport_approvalf, name='icnreport_approvalf'),
 path('icnreport_approvalt/<int:id>/<int:did>/', views.icnreport_approvalt, name='icnreport_approvalt'),
 path('icnreport_approvalm/<int:id>/<int:did>/', views.icnreport_approvalm, name='icnreport_approvalm'),
 path('activityreport_approvalt/<int:id>/<int:did>/', views.activityreport_approvalt, name='activityreport_approvalt'),
 path('activityreport_approvalm/<int:id>/<int:did>/', views.activityreport_approvalm, name='activityreport_approvalm'),
 path('activityreport_approvalp/<int:id>/<int:did>/', views.activityreport_approvalp, name='activityreport_approvalp'),
 path('activityreport_approvalf/<int:id>/<int:did>/', views.activityreport_approvalf, name='activityreport_approvalf'),
 path('icnreport_filter/', views.icnreport_filter, name='icnreport_filter'),
 path('activityreport_filter/', views.search_results_view2, name='activityreport_filter'),
 
 path('document_list/<int:id>/', views.document_list, name='icnreport_document_list'),
 path('activityreport_document_list/<int:id>/', views.activityreport_document_list, name='activityreport_document_list'),
 
 path('current_submit_approval_list/<int:id>/', views.current_submit_approval_list, name='icnreport_current_submit_approval_list'),
 path('latest_submit_approval_list/<int:id>/', views.latest_submit_approval_list, name='icnreport_latest_submit_approval_list'),
 path('latest_submit_approval_list_activity/<int:id>/', views.latest_submit_approval_list_activity, name='latest_submit_approval_list_reportactivity'),
 path('current_activityreport_submit_approval_list/<int:id>/', views.current_activityreport_submit_approval_list, name='current_activityreport_submit_approval_list'),
 path('icnreport_submit_approval_list/<int:id>/', views.submit_approval_list, name='icnreport_submit_approval_list'),
 path('activityreport_submit_approval_list/<int:id>/', views.activityreport_submit_approval_list, name='activityreport_submit_approval_list'),
 path('add_impact/<int:id>/', views.add_icnreport_impact, name='icnreport_add_impact'),
 path('add_activityreport_impact/<int:id>/', views.add_activityreport_impact, name='add_activityreport_impact'),
 path('impact_list/<int:id>/', views.icnreport_impact_list, name='icnreport_impact_list'),
 path('activityreport_impact_list/<int:id>/', views.activityreport_impact_list, name='activityreport_impact_list'),
 path('edit_impact/<int:pk>/', views.edit_impact, name='icnreport_edit_impact'),
 path('edit_activityreport_impact/<int:pk>/', views.edit_activityreport_impact, name='edit_activityreport_impact'),
 path('icnreport_impact/<int:pk>/remove/', views.icnreport_remove_impact, name='icnreport_remove_impact'),
 path('activityreport_impact/<int:pk>/remove', views.remove_activityreport_impact, name='remove_activityreport_impact'),
]

urlpatterns += htmxpatterns