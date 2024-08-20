"""
URL configuration for security project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from secman import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('logout', views.logout, name='logout'),
    path('companyList/',views.companyList,name='companyList'),
    path('add_company/', views.add_company, name='add_company'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_fo/', views.add_fo, name='add_fo'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('fo_dashboard/', views.fo_dashboard, name='fo_dashboard'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('create_quotation/', views.create_quotation, name='create_quotation'),
    path('addshift',views.addshift,name='addshift'),
    path('shifts/', views.shift_list, name='shift_list'),
    path('markattendance',views.markattendance, name='markattendance'),
    path('markattendance/submit/<int:employee_id>/', views.submit_attendance, name='submit_attendance'),
    
    path('admin/', admin.site.urls),
]
