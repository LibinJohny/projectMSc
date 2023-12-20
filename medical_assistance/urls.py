"""
URL configuration for medical_assistance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from medical_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('users-login/',views.users_login),
    #admin
    path('admin-dashboard/',views.admin_dashboard),
    path('admin-adddepartment/',views.admin_adddepartment),
    path('admin-viewdepartments/',views.admin_viewdepartments),
    path('admin-updatedepartment/',views.admin_updatedepartment),
    path('admin-deletedepartment/',views.admin_deletedepartment),
    path('admin-adddoctor/',views.admin_adddoctor),
    path('admin-viewdoctors/',views.admin_viewdoctors),
    path('admin-filterbydept/',views.admin_filterbydept),
    path('admin-viewsingledoctor/',views.admin_viewsingledoctor),
    path('admin-updatedoctor/',views.admin_updatedoctor),
    path('admin-deletedoctor/',views.admin_deletedoctor),
    path('admin-viewfeedbacks/',views.admin_viewfeedbacks),
    #user
    path('users-signup/',views.users_signup),
    path('user-dashboard/',views.user_dashboard),
    path('user-viewdoctors/',views.user_viewdoctors),
    path('user-filterbydept/',views.user_filterbydept),
    path('user-viewsingledoctor/',views.user_viewsingledoctor),
    path('user-makeappointment/',views.user_makeappointment),
    path('user-add-appointment/',views.user_add_appointment),
    path('user-viewappointments/',views.user_viewappointments),
    path('user-changeappointment/',views.user_changeappointment),
    path('user-deleteappointment/',views.user_deleteappointment),
    path('user-viewhistory/',views.user_viewhistory),
    path('user-addfeedback/',views.user_addfeedback),
    path('user-viewprofile/',views.user_viewprofile),
    path('user-updateprofile/',views.user_updateprofile),
    path('user-deleteprofile/',views.user_deleteprofile),
    path('chat/',views.chat),
    #doctor
    path('doctor-dashboard/',views.doctor_dashboard),
    path('doctor-viewappointments/',views.doctor_viewappointments),
    path('doctor-changeappointmentstatus/',views.doctor_changeappointmentstatus),
    path('doctor-viewfeedbacks/',views.doctor_viewfeedbacks),
]
