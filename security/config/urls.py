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
from secman import views , admin_views


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
    path('createquotation/', views.createquotation, name='createquotation'),
    path('addshift',views.addshift,name='addshift'),
    path('shifts/', views.shift_list, name='shift_list'),
    path('markattendance/', views.markattendance, name='markattendance'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('submit_attendance/<int:employee_id>/', views.submit_attendance, name='submit_attendance'),
    path('colist/',views.companyList,name='colist'),
    path('quotation', views.quotation, name='quotation'),
    path('quotation_list/', views.quotation_list, name='quotation_list'),
    path('view_quotation-pdf/<int:pk>/', views.view_quotation_pdf, name='view_quotation_pdf'),
    path('update-quotation/', views.update_quotation, name='update_quotation'),
    path('create-tax-invoice/', views.create_tax_invoice, name='create_tax_invoice'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:company_id>/', views.company_employees, name='company_employees'),
    path('salarysheet',views.salarysheet,name='salarysheet'),
    path('adsalarysheet',views.adminsalarysheet,name='adminsalarysheet'),
    path('present',views.present, name='present'),
    path('get-employees/', views.get_employees, name='get_employees'),
    path('monthly-attendance/<str:emp_id>/', views.monthly_attendance, name='monthly_attendance'),
    path('advance/<str:employee_id>/', views.advance, name='request_advance'),
    path('admin_advance/<str:employee_id>/', admin_views.admin_advance, name='admin_request_advance'),
    path('admin/', admin.site.urls),
    path('delete_quotation/<int:id>/', views.delete_quotation, name='delete_quotation'),
    path('addbirth/', views.addbirth, name='addbirth'),
    path('edit/<int:birthday_id>/', views.edit_birthday, name='edit_birthday'),
    path('delete/<int:birthday_id>/', views.delete_birthday, name='delete_birthday'),
    path('mess/<str:emp_id>/', views.mess_view, name='mess'),
    path('admin_mess/<str:emp_id>/', admin_views.admin_mess_view, name='admin_mess'),
    path('partial-uniform/<str:emp_id>/', views.partial_uniform_view, name='partial_uniform'),
    path('admin_partial-uniform/<str:emp_id>/', admin_views.admin_partial_uniform_view, name='admin_partial_uniform'),
    path('advance-requests/', views.advance_requests, name='advance_requests'),
    path('/approve-advance/<int:pk>/', views.approve_advance, name='approve_advance'),
    path('/reject-advance/<int:pk>/', views.reject_advance, name='reject_advance'),
    path('admin_addshift',admin_views.admin_addshift,name='admin_addshift'),
    path('admin_shifts/', admin_views.admin_shift_list, name='admin_shift_list'),
    path('admin_markattendance/', admin_views.admin_markattendance, name='admin_markattendance'),
    path('admin_submit_attendance/', admin_views.admin_submit_attendance, name='admin_submit_attendance'),
    path('admin_submit_attendance/<int:employee_id>/', admin_views.admin_submit_attendance, name='admin_submit_attendance'),
    path('admin_companies/', admin_views.admin_company_list, name='admin_company_list'),
    path('admin_companies/<int:company_id>/', admin_views.admin_company_employees, name='admin_company_employees'),
    path('admin_salarysheet',admin_views.admin_salarysheet,name='admin_salarysheet'),
    path('admin_present',admin_views.admin_present, name='admin_present'),
    path('admin_get-employees/', admin_views.admin_get_employees, name='admin_get_employees'),
    path('admin_monthly-attendance/<str:emp_id>/', admin_views.admin_monthly_attendance, name='admin_monthly_attendance'),
    path('admin_advance/<str:emp_id>/', admin_views.admin_advance_options, name='admin_advance'),
    path('update_salary/', views.update_salary, name='update_salary'),
    path('add_emp/', admin_views.add_emp, name='add_emp'),
    





]
