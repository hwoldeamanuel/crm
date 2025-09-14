from django.urls import path, include

from . import views




urlpatterns = [
   
    path('', views.conceptnotes, name='icns'),
    path('intervention/', views.conceptnotes, name='icns'),
    path('intervention/new/profile/', views.icn_add, name='icn_new'),
    path('intervention/<int:id>/profile/edit/', views.icn_edit, name='icn_edit'),
    path('intervention/<int:id>/impact/', views.icn_step_impact, name='icn_step_impact'),
    path('intervention/<int:id>/submission/', views.icn_step_submission, name='icn_step_submission'),
    path('intervention/<int:id>/approval/', views.icn_step_approval, name='icn_step_approval'),
    path('intervention/<int:id>/report/', views.icn_step_report, name='icn_step_report'),
    path('intervention/<int:id>/submission/list/', views.current_submit_list, name='current_submit_list'),
    path('activity/<int:id>/impact/', views.activity_step_impact, name='activity_step_imbpact'),
    path('intervention/<int:id>/intervention_step/', views.intervention_step, name='intervention_step'),
    path('icn/add', views.icn_add, name='icn_add'),
    path('icn_detail_modal/<int:id>/', views.icn_detail_modal, name='icn_detail_modal'),
    path('activity/<int:id>/approval/', views.activity_step_approval, name='activity_step_approval'),
    path('intervention/<int:pk>/profile/', views.icn_detail, name='icn_detail'),
    path('intervention/<int:pk>/approval/', views.icn_submit_approval, name='icn_submit_approval'),
    path('activity/<int:pk>/approval/', views.activity_submit_approval, name='activity_submit_approval'),
    path('download/<int:id>/', views.download, name='download'),
    path('downloada/<int:id>/', views.downloada, name='downloadacnd'),
    path('delete_icn/<int:pk>/', views.icn_delete, name='icn_delete'),
    path('delete_activity/<int:pk>/', views.activity_delete, name='activity_delete'),
    path('intervention/program_lead/', views.program_lead, name='program_lead'),
    path('icn_info/', views.icn_info, name='icn_info'),
    
    path('download_env_att/<int:id>/', views.download_env_att, name='download_env_att'),
    path('icn_submit_form_partial/<int:id>/', views.icn_submit_form_partial, name='icn_submit_form_partial'),
     
    path('icn_submit_form_partialm/<int:id>/', views.icn_submit_form_partialm, name='icn_submit_form_partialm'),
    
    path('icn_approvalp_form_partial/<int:id>/', views.icn_approvalp_form_partial, name='icn_approvalp_form_partial'),
    path('activity_submit_form_partial/<int:id>/', views.activity_submit_form_partial, name='activity_submit_form_partial'),
    path('activity/', views.activities, name='activities'),
    path('activity/<int:pk>/profile/', views.activity_detail, name='activity_detail'),
    path('activity/profile/new/', views.activity_add, name='activity_add'),
    path('activity/<int:id>/profile/edit/', views.activity_edit, name='activity_edit'),
    path('aregion/<int:id>/', views.aregion, name='aregion'),
    path('aregion/aedit_aarea/<int:pk>/', views.aarea_edit_form, name='aarea_edit_form'),
    path('intervention/program_changes/', views.program_changes, name='program_changes'),
   
]

htmxpatterns = [


 
 path('icn_submit_detail/<int:id>/', views.icn_submit_detail, name='icn_submit_detail'),
 path('icn_submit_list/<int:id>/', views.icn_submit_list, name='icn_submit_list'),
 path('icn_approval_invoice/<int:id>/', views.icn_approval_invoice, name='icn_approval_invoice'),
 path('activity_approval_invoice/<int:id>/', views.activity_approval_invoice, name='activity_approval_invoice'),
 path('icn_submit_form/<int:id>/<int:sid>/', views.icn_submit_form, name='icn_submit_form'),
 path('activity_submit_form/<int:id>/<int:sid>/', views.activity_submit_form, name='activity_submit_form'),
 path('icn_submit_document/<int:id>/', views.icn_submit_document, name='icn_submit_document'),
 path('activity_submit_document/<int:id>/', views.activity_submit_document, name='activity_submit_document'),
 path('icn_approvalp/<int:id>/<int:did>/', views.icn_approvalp, name='icn_approvalp'),
 path('icn_approvalf/<int:id>/<int:did>/', views.icn_approvalf, name='icn_approvalf'),
 path('icn_approvalt/<int:id>/<int:did>/', views.icn_approvalt, name='icn_approvalt'),
 path('icn_approvalm/<int:id>/<int:did>/', views.icn_approvalm, name='icn_approvalm'),
 path('activity_approvalt/<int:id>/<int:did>/', views.activity_approvalt, name='activity_approvalt'),
 path('activity_approvalm/<int:id>/<int:did>/', views.activity_approvalm, name='activity_approvalm'),
 path('activity_approvalp/<int:id>/<int:did>/', views.activity_approvalp, name='activity_approvalp'),
 path('activity_approvalf/<int:id>/<int:did>/', views.activity_approvalf, name='activity_approvalf'),
 path('icn_filter/', views.search_results_view, name='icn_filter'),
 path('activity_filter/', views.search_results_view2, name='activity_filter'),
 path('woredas/', views.iworedas, name='iworedas'),
 path('document_list/<int:id>/', views.document_list, name='document_list'),
 path('activity_document_list/<int:id>/', views.activity_document_list, name='activity_document_list'),
 path('iarea_list/<int:id>/', views.iarea_list, name='iarea_list'),
 path('aarea_list/<int:id>/', views.aarea_list, name='aarea_list'),
 path('current_submit_approval_list/<int:id>/', views.current_submit_approval_list, name='current_submit_approval_list'),
 path('current_activity_submit_approval_list/<int:id>/', views.current_activity_submit_approval_list, name='current_activity_submit_approval_list'),
 path('icn_submit_approval_list/<int:id>/', views.icn_submit_approval_list, name='icn_submit_approval_list'),
 path('activity_submit_approval_list/<int:id>/', views.activity_submit_approval_list, name='activity_submit_approval_list'),
 path('add_impact/<int:id>/', views.add_impact, name='add_impact'),
 path('add_activity_impact/<int:id>/', views.add_activity_impact, name='add_activity_impact'),
 path('impact_list/<int:id>/', views.impact_list, name='impact_list'),
 path('activity_impact_list/<int:id>/', views.activity_impact_list, name='activity_impact_list'),
 path('icn_edit_impact/<int:pk>/', views.icn_edit_impact, name='icn_edit_impact'),
 path('icn_add_disaggregate/<int:id>/', views.add_disaggregate, name='icn_add_disaggregate'),
 path('icn_edit_disaggregate/<int:pk>/', views.edit_disaggregate, name='icn_edit_disaggregate'),
 path('icn_delete_disaggregate/<int:pk>/', views.delete_disaggregate, name='icn_delete_disaggregate'),
 path('edit_activity_impact/<int:pk>/', views.edit_activity_impact, name='edit_activity_impact'),
 path('impact/<int:pk>/remove/', views.remove_impact, name='remove_impact'),
 path('activity_impact/<int:pk>/remove', views.remove_activity_impact, name='remove_activity_impact'),
 
 path('add_impact_form/', views.add_impact_form, name='add_impact_form'),
 path('iworedas/', views.iworedas, name='iworedas'),
 
]

urlpatterns += htmxpatterns