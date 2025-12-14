from django.urls import path, include

from . import views




urlpatterns = [
   
    path('', views.travel, name='travel'),
    path('request/<int:id>/detail/', views.trequest_detail, name='trequest_detail'),
    path('request/<int:id>/cost/', views.trequest_cost, name='trequest_cost'),
    path('request/new/', views.trequest_new, name='trequest_new'),
    path('request/<int:id>/edit/', views.trequest_edit, name='trequest_edit'),
    path('request/<int:id>/review/', views.trequest_review, name='trequest_review'),
    path('request/<int:id>/approval/', views.trequest_approval, name='trequest_approval'),
    path('request/<int:id>/approval/invoice/', views.trequest_approval_invoice, name='trequest_approval_invoice'),
    
]

htmxpatterns = [


   path('add_travel_cost/<int:id>/', views.add_travel_cost, name='add_travel_cost'),  
   path('edit_travel_cost/<int:id>/', views.edit_travel_cost, name='edit_travel_cost'),
   path('travel_cost_detail/<int:id>/', views.travel_cost_detail, name='travel_cost_detail'), 
   path('delete_travel_cost/<int:id>/', views.delete_travel_cost, name='delete_travel_cost'),  
   path('add_finance_code/<int:id>/', views.add_finance_code, name='add_finance_code'),  
   path('edit_finance_code/<int:id>/', views.edit_finance_code, name='edit_finance_code'),
   path('finance_code_detail/<int:id>/', views.finance_code_detail, name='finance_code_detail'), 
   path('delete_finance_code/<int:id>/', views.delete_finance_code, name='delete_finance_code'),            
   path('cost_list/<int:id>/', views.cost_list, name='cost_list'), 
   path('finance_list/<int:id>/', views.finance_list, name='finance_list'), 
   path('lincodes/', views.lincodes, name='lincodes'), 
   path('submit_request/<int:id>/<int:sid>/', views.submit_request, name='submit_request'), 
   path('edit_request/<int:id>/<int:sid>/', views.edit_request, name='edit_request'), 
   path('submit_approval_list/<int:id>/', views.submit_approval_list, name='submit_approval_list'),
   path('approval_list/<int:id>/', views.approval_list, name='approval_list'),  
   path('approve_requestb/<int:id>/<int:aid>/', views.approve_requestb, name='approve_requestb'), 
   path('approve_requestf/<int:id>/<int:aid>/', views.approve_requestf, name='approve_requestf'), 
   path('approve_requests/<int:id>/<int:aid>/', views.approve_requests, name='approve_requests'), 
   path('request_filter/', views.request_filter, name='request_filter'), 
   path('add_travel_costp/<int:id>/', views.add_travel_costp, name='add_travel_costp'),  
   path('edit_travel_costp/<int:id>/', views.edit_travel_costp, name='edit_travel_costp'),
]

urlpatterns += htmxpatterns