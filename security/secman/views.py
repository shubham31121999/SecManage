from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Company


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def dashboardco(request):
    return render(request, 'company/baseco.html')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        logger.debug(f'Received POST request with email: {email} and password: {password}')
        
        if not email or not password:
            messages.error(request, 'Email and password fields cannot be empty')
            logger.error('Email or password fields were empty')
            return render(request, 'login.html')
        
        user = authenticate(request, email=email, password=password)
        logger.debug(f'Authentication result: {user}')
        
        if user is not None:
            auth_login(request, user)
            logger.info(f'User {user} logged in successfully')
            return redirect('dashboard')  # Ensure 'dashboard' is a valid URL name
        else:
            messages.error(request, 'Invalid email or password')
            logger.error('Invalid email or password')
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout






@login_required
def add_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        company_contact = request.POST.get('company_contact')
        gst_number = request.POST.get('gst_number')

        if company_name and company_address and company_contact and gst_number:
            Company.objects.create(
                company_name=company_name,
                company_address=company_address,
                company_contact=company_contact,
                gst_number=gst_number,
                user=request.user
            )
            return redirect('companyList')  # Redirect to a company list page or wherever appropriate
    return render(request, 'admin/add_company.html')

def companyList(request):
    companies = Company.objects.filter(user=request.user)
    return render(request, 'admin/companyList.html', {'companies': companies})


