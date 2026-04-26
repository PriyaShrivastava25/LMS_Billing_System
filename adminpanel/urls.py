from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('enrollments/', views.manage_enrollments, name='manage_enrollments'),
    path('invoices/', views.manage_invoices, name='manage_invoices'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),



]
