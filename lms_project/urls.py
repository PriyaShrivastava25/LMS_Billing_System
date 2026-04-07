"""
URL configuration for lms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard.views import home, login_view, signup, student_dashboard, logout_view, view_invoice
from resources.views import course_list, enroll_course
from billing.views import download_invoice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('courses/', course_list, name='course_list'),
    path('courses/enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('logout/', logout_view, name='logout'),
     path('invoice/<int:invoice_id>/', view_invoice, name='view_invoice'),
     path('download-invoice/<int:invoice_id>/', download_invoice, name='download_invoice'),
]



