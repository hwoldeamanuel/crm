from django.urls import path, include

from . import views




urlpatterns = [
   
    path('', views.carm, name='carm'),
    path('feedback/', views.carm, name='carm'),
    path('feedback/new/', views.feedback_add, name='feedback_add'),
    path('feedback/<int:id>/detail/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:id>/edit/', views.feedback_edit, name='feedback_edit'),
    path('feedback/<int:id>/processing/', views.feedback_processing, name='feedback_processing'),
    path('feedback/<int:id>/processing/new/', views.feedback_processing_add, name='feedback_processing_add'),
    path('email/',views.emailbar, name='email'),
    path('download_feedback_att/<int:id>/', views.download_feedback_att, name='download_feedback_att'),
    path('feedback/<int:id>/processing/edit/', views.feedback_processing_edit, name='feedback_processing_edit'),
    path('feedback/<int:id>/closing/', views.feedback_closing, name='feedback_closing'),
    path('feedback/<int:id>/closing/new/', views.feedback_closing_add, name='feedback_closing_add'),
    path('feedback/<int:id>/closing/edit/', views.feedback_closing_edit, name='feedback_closing_edit'),
    
    ]