from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest
from django.core.files.base import ContentFile
from datetime import datetime, timedelta, time
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import EmployeeJoining, UserProfile,ShiftTime,Attendance,SalaryDetails
from django.db import IntegrityError
from django.contrib.staticfiles import finders
from .models import UserProfile, Quotation
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, F, ExpressionWrapper, fields, DurationField
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render
from datetime import datetime
from .models import SalaryDetails, Attendance
from django.db.models import Count
import io
from django.shortcuts import render
from django.db.models import Count, F, Sum
from datetime import timedelta

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import EmployeeJoining, Attendance
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Attendance, EmployeeJoining
from django.views.decorators.http import require_POST
from django.db import IntegrityError


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Attendance, EmployeeJoining
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Attendance, EmployeeJoining
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import EmployeeJoining, Attendance,SalaryDetails
from django.core.exceptions import ValidationError

import inflect









def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate using the email field, which acts as the username
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on the user type
                if user.is_superuser:
                    return redirect('dashboard')

                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.user_type == 'company':
                        return redirect('company_dashboard')
                    elif user_profile.user_type == 'fo':
                        return redirect('fo_dashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, "User profile not found.")
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')



def logout(request):
    auth_logout(request)
    return redirect('login') 


def dashboard(request):
    return render(request, 'admin/dashboard.html')


def company_dashboard(request):
    return render(request, 'company/company_dashboard.html')


from django.shortcuts import render
from datetime import timedelta
from .models import EmployeeJoining, Attendance

def fo_dashboard(request):
    employees = EmployeeJoining.objects.all()

    employee_hours = []

    for employee in employees:
        # Get the number of attendance records with status 'P' (Present)
        num_present_days = Attendance.objects.filter(employee=employee, status='P').count()

        # Get the shift time for the employee, assuming a single shift for simplicity
        shifts = Attendance.objects.filter(employee=employee, status='P').values_list('shift', flat=True).distinct()
        if shifts:
            shift = ShiftTime.objects.filter(id__in=shifts).first()
            shift_time = shift.shift_total_time if shift else timedelta()
        else:
            shift_time = timedelta()

        # Calculate total worked hours
        total_worked_time = num_present_days * shift_time

        employee_hours.append({
            'employee': employee,
            'total_hours': total_worked_time
        })

    return render(request, 'FO/fo_dashboard.html', {'employee_hours': employee_hours})




#########################################################################################################

def add_company(request):
    if request.method == "POST":
        # Debug: Print the POST data to check what is being received
        print(request.POST)

        # Use get() to safely retrieve form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        gst_or_emergency = request.POST.get('gst_or_emergency')

        # Check if all required fields are provided
        if not email or not password or not first_name or not last_name:
            return render(request, 'admin/add_company.html', {'error': 'All fields are required.'})

        # Create the user and user profile
        user = User.objects.create_user(
            username=email,  # Use email as the username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        UserProfile.objects.create(
            user=user,
            user_type='company',
            contact=contact,
            gst_or_emergency=gst_or_emergency,
        )
        return redirect('dashboard')  # Redirect to the dashboard or another page

    return render(request, 'admin/add_company.html')


# def add_company(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         contact = request.POST['contact']
#         gst_or_emergency = request.POST['gst_or_emergency']

#         user = User.objects.create_user(
#             username=email,  # Use email as the username
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         UserProfile.objects.create(
#             user=user,
#             user_type='company',
#             contact=contact,
#             gst_or_emergency=gst_or_emergency,
#         )
#         return redirect('dashboard')  # Redirect to login or wherever you need

#     return render(request, 'admin/add_company.html')

#####################################################################################################################################

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile

def add_fo(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact = request.POST['contact']
        gst_or_emergency = request.POST['gst_or_emergency']

        try:
            # Create a new user
            user = User.objects.create_user(
                username=email,  # Use email as the username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create a user profile linked to the user
            UserProfile.objects.create(
                user=user,
                user_type='fo',  # Assuming 'fo' is the user type for the FO role
                contact=contact,
                gst_or_emergency=gst_or_emergency,
            )

            return redirect('dashboard')  # Redirect to the dashboard after successful creation

        except IntegrityError:
            # Handle the case where the username (email) is already in use
            return render(request, 'admin/add_fo.html', {
                'error': 'A user with this email already exists.'
            })

    return render(request, 'admin/add_fo.html')

# def add_fo(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         contact = request.POST['contact']
#         gst_or_emergency = request.POST['gst_or_emergency']

#         user = User.objects.create_user(
#             username=email,  # Use email as the username
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         UserProfile.objects.create(
#             user=user,
#             user_type='fo',
#             contact=contact,
#             gst_or_emergency=gst_or_emergency,
#         )
#         return redirect('dashboard')  # Redirect to login or wherever you need

#     return render(request, 'admin/add_fo.html')

def companyList(request):
    companies = UserProfile.objects.filter(user_type='company')
    return render(request, 'admin/companyList.html', {'companies': companies})


############################################   Employee Joining Form   #####################################################





def add_employee(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Employee data
                emp_id = request.POST['emp_id']
                first_name = request.POST['first_name']
                middle_name = request.POST.get('middle_name', '')
                last_name = request.POST['last_name']
                email = request.POST['email']
                contact_number = request.POST['contact_number']
                whatsapp_number = request.POST.get('whatsapp_number', '')
                age = request.POST['age']
                gender = request.POST['gender']
                current_address = request.POST['current_address']
                permanent_address = request.POST['permanent_address']
                city = request.POST['city']
                state = request.POST['state']
                pincode = request.POST['pincode']
                date_of_birth = request.POST['date_of_birth']
                emergency_contact1 = request.POST['emergency_contact1']
                emergency_contact2 = request.POST['emergency_contact2']
                emergency_contact_relation1 = request.POST['emergency_contact_relation1']
                emergency_contact_relation2 = request.POST['emergency_contact_relation2']
                emergency_contact_relation1_address = request.POST['emergency_contact_relation1_address']
                emergency_contact_relation2_address = request.POST['emergency_contact_relation2_address']
                pancard = request.POST['pancard']
                aadhar = request.POST['aadhar']
                voter = request.POST['voter']
                security_guard_training = request.POST.get('security_guard_training') == 'yes'
                job_experience = request.POST.get('job_experience') == 'yes'
                profile_picture = request.FILES['profile_picture']
                signature = request.FILES['signature']
                preferred_work_arrangements = request.POST['preferred_work_arrangements']
                position = request.POST['position']
                account_holder_name = request.POST['account_holder_name']
                bank_name = request.POST['bank_name']
                bank_account_number = request.POST['bank_account_number']
                ifsc_code = request.POST['ifsc_code']
                branch_name = request.POST['branch_name']
                bank_address = request.POST['bank_address']
                qualification = request.POST['qualification']
                experience = request.POST['experience']
                
                

                # Company data
                company_id = request.POST.get('company')
                company = None
                if company_id:
                    try:
                        company = UserProfile.objects.get(id=company_id, user_type='company')
                    except UserProfile.DoesNotExist:
                        return render(request, 'FO/employee_form.html', {'error': 'Selected company does not exist or is not valid.'})

        try:
            employee = EmployeeJoining(
                emp_id=emp_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                contact_number=contact_number,
                whatsapp_number=whatsapp_number,
                age=age,
                gender=gender,
                current_address=current_address,
                permanent_address=permanent_address,
                city=city,
                state=state,
                pincode=pincode,
                security_guard_training=security_guard_training,
                job_experience=job_experience,
                profile_picture=profile_picture,
                date_of_birth=date_of_birth,
                emergency_contact1=emergency_contact1,
                emergency_contact2=emergency_contact2,
                emergency_contact_relation1=emergency_contact_relation1,
                emergency_contact_relation2=emergency_contact_relation2,
                emergency_contact_relation1_address=emergency_contact_relation1_address,
                emergency_contact_relation2_address=emergency_contact_relation2_address,
                pancard=pancard,
                aadhar=aadhar,
                voter=voter,
                signature=signature,
                preferred_work_arrangements=preferred_work_arrangements,
                position=position,
                account_holder_name=account_holder_name,
                bank_name=bank_name,
                bank_account_number=bank_account_number,
                ifsc_code=ifsc_code,
                branch_name=branch_name,
                bank_address=bank_address,
                qualification=qualification,
                experience=experience,
                company=company,  # Assign the selected company to the employee
                basic_salary=basic_salary,
                special_allowance=special_allowance,
                conveyance_allowance=conveyance_allowance,
                education_allowance=education_allowance,
                travelling_allowance=travelling_allowance,
                hours_daily_duty=hours_daily_duty,
                total=total,
                hra=hra,
                pf=pf,
                gratuity=gratuity,
                leave_with_wages=leave_with_wages,
                esic=esic,
                paid_holiday=paid_holiday,
                bonus=bonus,
                uniform=uniform,
                total_b=total_b,
                total_c=total_c,
                service_charge=service_charge,
                shift=shift,
            )
            employee.save()

                # Generate PDF
                pdf_data = generate_employee_pdf(employee)

                # Save PDF to the model instance
                employee.pdf_file.save(f'{employee.emp_id}_details.pdf', ContentFile(pdf_data))

                # Provide the generated PDF for download
                response = HttpResponse(pdf_data, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{employee.emp_id}_details.pdf"'

                return response
        except IntegrityError:
            return render(request, 'FO/employee_form.html', {'error': 'Employee ID already exists. Please use a unique Employee ID.'})

    # If GET request, render the form with a list of companies
    companies = UserProfile.objects.filter(user_type='company')
    shifts = ShiftTime.objects.all()
    return render(request, 'FO/employee_form.html', {'companies': companies,'shifts': shifts})



# def generate_employee_pdf(employee):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
    
#     # Register custom font
#     # pdfmetrics.registerFont(TTFont('NotoSansDevanagari','C:/Users/PC/Desktop/SecManage/security/secman/static/NotoSansDevanagari-VariableFont_wdth,wght.ttf'))
#     font_path = finders.find('NotoSansDevanagari-VariableFont_wdth,wght.ttf')
#     # Define a custom style using the custom font
#     custom_style = ParagraphStyle(name='CustomStyle', parent=styles['Normal'], fontName='NotoSansDevanagari')
#     custom_style1 = ParagraphStyle(name='CustomStyle1', parent=styles['Heading2'], fontName='NotoSansDevanagari')
    
#     styles['Heading1'].fontName = 'Helvetica-Bold'
#     styles['Heading1'].fontSize = 20
#     styles['Heading1'].alignment = 1

#     styles['Heading2'].fontName = 'Helvetica-Bold'
#     styles['Heading2'].fontSize = 16
#     styles['Heading2'].alignment = 1

#     styles['Heading4'].fontName = 'Helvetica-Bold'
#     styles['Heading4'].fontSize = 12
#     styles['Heading4'].alignment = 1

#     styles['Normal'].alignment = 1
#     # Create the elements list to hold all the components of the PDF
#     elements = []

#     # Add headings
#     elements.append(Paragraph("Apollo Group", styles['Heading1']))
#     elements.append(Spacer(1, -15))  # Adjust vertical spacing
#     elements.append(Paragraph("Best Security Service", styles['Heading2']))
#     elements.append(Spacer(1, -10))  # Adjust vertical spacing
#     elements.append(Paragraph("Total Protection", styles['Heading4']))
#     elements.append(Spacer(1, 3))  # Adjust vertical spacing


#     elements.append(Paragraph('________________________________________________________________________________', styles['Normal']))
#     elements.append(Spacer(1, 8))

#     elements.append(Paragraph('________________________________________________________________________________', styles['Normal']))
#     elements.append(Spacer(1, -15))

#     # Dummy address centered
#     dummy_address = "1234 Apollo Street, Apollo City, Apollo Country - 123456"
#     elements.append(Paragraph(dummy_address, styles['Normal']))
#     elements.append(Spacer(1, 10))

#     # Add another horizontal line centered
#     # elements.append(Paragraph('________________________________________________________________________________', styles['Normal']))
#     # elements.append(Spacer(1, 10))
    

#     # Add heading "Joining Form"
#     elements.append(Paragraph("Joining Form", styles['Title']))
#     elements.append(Spacer(1, 12))

#     # Profile Picture
#     profile_img = None
#     if employee.profile_picture:
#         profile_img = Image(employee.profile_picture, width=1*inch, height=1*inch)

#     # Create a box for profile picture
#     profile_picture_box = Table([[profile_img if profile_img else '']], colWidths=[100])
#     profile_picture_box.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('BOX', (0, 0), (-1, -1), 1, 'black'),  # Add box with lines from all sides
#     ]))

#     # Employee details table
#     employee_details_data = [
#         [Paragraph(f"<b>Name:</b> {employee.first_name}", custom_style)],
#         [Paragraph(f"<b>पालकांचे नाव::</b> {employee.middle_name} {employee.last_name}", custom_style)],
#         [Paragraph(f"<b>सध्याचा पत्ता:</b> {employee.current_address}", custom_style)],
#         [Paragraph(f"<b>स्थायी पत्ता:</b> {employee.permanent_address}", custom_style)],
#     ]

#     # Create employee details table
#     employee_details_table = Table(employee_details_data, colWidths=[400])
#     employee_details_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('LINEBELOW', (0, 0), (-1, -1), 1, 'black'),  # Add horizontal line below each cell
#     ]))

#     # Combine profile picture box and employee details table
#     profile_and_details_data = [
#         [ employee_details_table,profile_picture_box]
#     ]
#     profile_and_details_table = Table(profile_and_details_data, colWidths=[400, 100])
#     profile_and_details_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(profile_and_details_table)
#     elements.append(Spacer(1, 12))

#     # Contact Number section
#     contact_number_section_data = [
#         [
#             Paragraph("<b>मोबाईल क्रमांक.:</b>", custom_style1),
#             Table([[Paragraph(f"<b>{digit}</b>", styles['Normal']) for digit in str(employee.contact_number)]], colWidths=[30]*10, style=[
#                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#                 ('INNERGRID', (0, 0), (-1, -1), 1, 'black'),  # Add inner grid lines
#                 ('BOX', (0, 0), (-1, -1), 1, 'black'),  # Add outer box lines
#             ])
#         ]
#     ]

#     contact_number_section_table = Table(contact_number_section_data, colWidths=[100, 400])
#     contact_number_section_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(contact_number_section_table)
#     elements.append(Spacer(1, 12))

#     # Married Status
#     married_status_data = [
#         [
#             Paragraph("<b>वैवाहिक स्थिती:</b>", custom_style1),
#             Paragraph("Yes" if employee.security_guard_training else "No", styles['Heading3']),  # Assuming married_status is a boolean field
#               # Assuming 'married_status' is a field in your employee model
#         ]
#     ]

#     married_status_table = Table(married_status_data, colWidths=[100, 400])
#     married_status_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(married_status_table)
#     elements.append(Spacer(1, 12))

#     qualification_data = [
#         [
#             Paragraph("<b>शिक्षण:</b>", custom_style1),
#             Paragraph( employee.qualification, styles['Heading3']),  # Assuming married_status is a boolean field
#               # Assuming 'married_status' is a field in your employee model
#         ]
#     ]

#     qualification_data_table = Table(qualification_data, colWidths=[100, 400])
#     qualification_data_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(qualification_data_table)
#     elements.append(Spacer(1, 12))


#     birth_data = [
#         [
#             Paragraph("<b>जन्मतारीख:</b>", custom_style1),
#             Paragraph( employee.date_of_birth, styles['Heading3']),  # Assuming married_status is a boolean field
#               # Assuming 'married_status' is a field in your employee model
#         ]
#     ]

#     birth_table = Table(birth_data, colWidths=[100, 400])
#     birth_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(birth_table)
#     elements.append(Spacer(1, 12))

#     document_data = [
#         [
#             Paragraph("<b>Pancard:</b>", custom_style1),
#             Paragraph("Yes" if employee.pancard else "No", styles['Heading3'])],  # Assuming married_status is a boolean field
#         [   Paragraph("<b>Aadhar Card:</b>", custom_style1),
#             Paragraph("Yes" if employee.aadhar else "No", styles['Heading3'])],  # Assuming married_status is a boolean field
#         [   Paragraph("<b>Voter ID:</b>",custom_style1 ),
#             Paragraph("Yes" if employee.voter else "No",styles['Heading3'] ),  # Assuming married_status is a boolean field
#               # Assuming 'married_status' is a field in your employee model
#         ]
#     ]

#     document_table = Table(document_data, colWidths=[100, 400])
#     document_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))

#     elements.append(document_table)
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph("<b>Emergency Contact</b>", styles['Heading3']))
#     elements.append(Spacer(1, 6))

#     # Emergency contact table with dummy data
#     emergency_contact_data = [
#         ["Name","Mobile Number","Address"],
#         [employee.emergency_contact_relation1, employee.emergency_contact1,employee.emergency_contact_relation1_address],
#         [employee.emergency_contact_relation1, employee.emergency_contact2,employee.emergency_contact_relation1_address],
#     ]
#     emergency_contact_table = Table(emergency_contact_data, colWidths=[2*inch, 2.5*inch,2.5*inch])
#     emergency_contact_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BOX', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(emergency_contact_table)
#     elements.append(Spacer(1, 45))

#     elements.append(Paragraph("<b>नियम व अटी :</b>", custom_style1))
#     elements.append(Spacer(1, 9))

#     # Dummy rules list
#     dummy_rules = [
#     "१) १५ दिवसांच्या आत काम सोडल्यास पेमेंट मिळणार नाही.",
#     "२) न सांगता ड्युटीवर न आल्यास पर डे १००/- दंड बसेल.",
#     "३) ड्युटीवर दारु पिऊन आल्यास कुठल्याही प्रकारचे पेमेंट मिळणार नाही व कामावरून कमी करण्यास येईल.",
#     "४) न सांगता ४ दिवस ड्युटीवरती न आल्यास कामवरुन कमी करण्यात येईल.",
#     "१) बघुटीवर असताना पुर्ण युनिफार्म असणे बंधनकारक आहे.",
#     "६) काम सोडायचे असल्यास १५ दिवस आगोदर राजीनामा देणे बंधनकारक आहे. न दिल्यास पहिले काम केलेले पेमेंट मिळणार नाही.",
#     "७) कामावरती कुठल्याही प्रकारचे गैरवर्तन आढळल्यास लगेच कामावरून कमी करण्यात येईल.",
#     "८) संस्थेची नोकरी कायमस्वरुपी नाही हे मला माहित आहे. संस्थेकडील ज्या कंत्राटामध्ये मी कामवर असेल ते कंत्राट बंद झाल्यास व दुसऱ्या ठिकाणी जागा रिकामी नसल्यास मला नोकरी वरून काढले जाईल हे मला मान्य आहे.",
#     "९) ड्युटीवर असताना झोपेत सापडल्यास ५००/- दंड बसेल.",
#     "१०) कंपनीने दिलेले हे सर्व नियम मला मान्य आहेत.",
#     ]

#     # Add dummy rules point-wise
#     for rule in enumerate(dummy_rules):
#         elements.append(Paragraph(f"{rule}", custom_style))
#         elements.append(Spacer(1, 6))


#     elements.append(Paragraph("<b>Left Finger</b>", styles['Heading3']))
#     elements.append(Spacer(1, 6))

#     # Add boxes for left finger with spaces between
#     left_finger_data = [
#         ["", "", "", "", ""]
#     ]
#     left_finger_table = Table(left_finger_data, colWidths=[1*inch]*5, rowHeights=[1*inch])
#     # left_finger_table = Table(left_finger_data, colWidths=[1*inch]*5)
#     left_finger_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),  # Add inner grid lines
#         ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Add outer box lines
#     ]))

#     elements.append(left_finger_table)
#     elements.append(Spacer(1, 12))


#     elements.append(Paragraph("<b>Right Finger</b>", styles['Heading3']))
#     elements.append(Spacer(1, 6))

#     # Add boxes for left finger with spaces between
#     right_finger_data = [
#         ["", "", "", "", ""]
#     ]
#     right_finger_table = Table(right_finger_data, colWidths=[1*inch]*5, rowHeights=[1*inch])
#     # left_finger_table = Table(left_finger_data, colWidths=[1*inch]*5)
#     right_finger_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),  # Add inner grid lines
#         ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Add outer box lines
#     ]))

#     elements.append(right_finger_table)
#     elements.append(Spacer(1, 72))


#     # Signature, place, and date table
#     signature_table_data = [
#         [
#             Paragraph("<b>Date:</b> ___________________", styles['Normal']),
#             Paragraph("<b>Signature:</b> ___________________", styles['Normal']),
#         ]
#     ]
#     signature_table = Table(signature_table_data, colWidths=[200,200])
#     signature_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('GRID', (0, 0), (-1, -1), 0, 'white'),  # Remove grid lines
#     ]))

#     elements.append(signature_table)

#     # Build PDF
#     doc.build(elements)
#     pdf_value = buffer.getvalue()
#     buffer.close()

#     return pdf_value

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from django.contrib.staticfiles import finders
from django.http import HttpResponse

def generate_employee_pdf(employee):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Find the font file
    font_path = finders.find('NotoSansDevanagari-VariableFont_wdth,wght.ttf')
    if not font_path:
        raise FileNotFoundError("Font file not found. Please ensure it's placed correctly in the static directory.")

    # Register custom font
    pdfmetrics.registerFont(TTFont('NotoSansDevanagari', font_path))

    # Define custom styles
    custom_style = ParagraphStyle(name='CustomStyle', parent=styles['Normal'], fontName='NotoSansDevanagari')
    custom_style1 = ParagraphStyle(name='CustomStyle1', parent=styles['Heading2'], fontName='NotoSansDevanagari')

    # Update default styles
    styles['Heading1'].fontName = 'Helvetica-Bold'
    styles['Heading1'].fontSize = 20
    styles['Heading1'].alignment = 1

    styles['Heading2'].fontName = 'Helvetica-Bold'
    styles['Heading2'].fontSize = 16
    styles['Heading2'].alignment = 1

    styles['Heading4'].fontName = 'Helvetica-Bold'
    styles['Heading4'].fontSize = 12
    styles['Heading4'].alignment = 1

    styles['Normal'].alignment = 1

    # Create PDF elements
    elements = []

    # Add headings and spacers
    elements.append(Paragraph("Apollo Group", styles['Heading1']))
    elements.append(Spacer(1, -15))
    elements.append(Paragraph("Best Security Service", styles['Heading2']))
    elements.append(Spacer(1, -10))
    elements.append(Paragraph("Total Protection", styles['Heading4']))
    elements.append(Spacer(1, 3))

    elements.append(Paragraph('________________________________________________________________________________', styles['Normal']))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('________________________________________________________________________________', styles['Normal']))
    elements.append(Spacer(1, -15))

    # Dummy address
    dummy_address = "1234 Apollo Street, Apollo City, Apollo Country - 123456"
    elements.append(Paragraph(dummy_address, styles['Normal']))
    elements.append(Spacer(1, 10))

    # Add heading "Joining Form"
    elements.append(Paragraph("Joining Form", styles['Title']))
    elements.append(Spacer(1, 12))

    # Profile Picture
    profile_img = None
    if employee.profile_picture:
        profile_img = Image(employee.profile_picture, width=1*inch, height=1*inch)
    
    profile_picture_box = Table([[profile_img if profile_img else '']], colWidths=[100])
    profile_picture_box.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, 'black'),
    ]))

    # Employee details table
    employee_details_data = [
        [Paragraph(f"<b>Name:</b> {employee.first_name}", custom_style)],
        [Paragraph(f"<b>पालकांचे नाव:</b> {employee.middle_name} {employee.last_name}", custom_style)],
        [Paragraph(f"<b>सध्याचा पत्ता:</b> {employee.current_address}", custom_style)],
        [Paragraph(f"<b>स्थायी पत्ता:</b> {employee.permanent_address}", custom_style)],
    ]
    
    employee_details_table = Table(employee_details_data, colWidths=[400])
    employee_details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 1, 'black'),
    ]))

    # Combine profile picture box and employee details table
    profile_and_details_data = [
        [employee_details_table, profile_picture_box]
    ]
    profile_and_details_table = Table(profile_and_details_data, colWidths=[400, 100])
    profile_and_details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(profile_and_details_table)
    elements.append(Spacer(1, 12))

    # Contact Number section
    contact_number_section_data = [
        [
            Paragraph("<b>मोबाईल क्रमांक:</b>", custom_style1),
            Table([[Paragraph(f"<b>{digit}</b>", styles['Normal']) for digit in str(employee.contact_number)]], colWidths=[30]*10, style=[
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 1, 'black'),
                ('BOX', (0, 0), (-1, -1), 1, 'black'),
            ])
        ]
    ]
    
    contact_number_section_table = Table(contact_number_section_data, colWidths=[100, 400])
    contact_number_section_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(contact_number_section_table)
    elements.append(Spacer(1, 12))

    # Married Status
    married_status_data = [
        [
            Paragraph("<b>वैवाहिक स्थिती:</b>", custom_style1),
            Paragraph("Yes" if employee.security_guard_training else "No", styles['Heading3']),
        ]
    ]
    
    married_status_table = Table(married_status_data, colWidths=[100, 400])
    married_status_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(married_status_table)
    elements.append(Spacer(1, 12))

    # Qualification
    qualification_data = [
        [
            Paragraph("<b>शिक्षण:</b>", custom_style1),
            Paragraph(employee.qualification, styles['Heading3']),
        ]
    ]
    
    qualification_data_table = Table(qualification_data, colWidths=[100, 400])
    qualification_data_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(qualification_data_table)
    elements.append(Spacer(1, 12))

    # Birth Date
    birth_data = [
        [
            Paragraph("<b>जन्मतारीख:</b>", custom_style1),
            Paragraph(employee.date_of_birth, styles['Heading3']),
        ]
    ]
    
    birth_table = Table(birth_data, colWidths=[100, 400])
    birth_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(birth_table)
    elements.append(Spacer(1, 12))

    # Document Details
    document_data = [
        [
            Paragraph("<b>Pancard:</b>", custom_style1),
            Paragraph("Yes" if employee.pancard else "No", styles['Heading3']),
        ],
        [
            Paragraph("<b>Aadhar Card:</b>", custom_style1),
            Paragraph("Yes" if employee.aadhar else "No", styles['Heading3']),
        ],
        [
            Paragraph("<b>Voter ID:</b>", custom_style1),
            Paragraph("Yes" if employee.voter else "No", styles['Heading3']),
        ]
    ]
    
    document_table = Table(document_data, colWidths=[100, 400])
    document_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(document_table)
    elements.append(Spacer(1, 12))

    # Emergency Contact
    elements.append(Paragraph("<b>Emergency Contact</b>", styles['Heading3']))
    elements.append(Spacer(1, 6))

    emergency_contact_data = [
        ["Name", "Mobile Number", "Address"],
        [employee.emergency_contact_relation1, employee.emergency_contact1, employee.emergency_contact_relation1_address],
        [employee.emergency_contact_relation2, employee.emergency_contact2, employee.emergency_contact_relation2_address],
    ]
    emergency_contact_table = Table(emergency_contact_data, colWidths=[2*inch, 2.5*inch, 2.5*inch])
    emergency_contact_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(emergency_contact_table)
    elements.append(Spacer(1, 45))

    # Rules
    elements.append(Paragraph("<b>नियम व अटी :</b>", custom_style1))
    elements.append(Spacer(1, 9))

    dummy_rules = [
        "१) १५ दिवसांच्या आत काम सोडल्यास पेमेंट मिळणार नाही.",
        "२) न सांगता ड्युटीवर न आल्यास पर डे १००/- दंड बसेल.",
        "३) ड्युटीवर दारु पिऊन आल्यास कुठल्याही प्रकारचे पेमेंट मिळणार नाही व कामावरून कमी करण्यास येईल.",
        "४) न सांगता ४ दिवस ड्युटीवरती न आल्यास कामावरुन कमी करण्यात येईल.",
        "५) बघुटीवर असताना पुर्ण युनिफार्म असणे बंधनकारक आहे.",
        "६) काम सोडायचे असल्यास १५ दिवस आगोदर राजीनामा देणे बंधनकारक आहे. न दिल्यास पहिले काम केलेले पेमेंट मिळणार नाही.",
        "७) कामावरती कुठल्याही प्रकारचे गैरवर्तन आढळल्यास लगेच कामावरून कमी करण्यात येईल.",
        "८) संस्थेची नोकरी कायमस्वरुपी नाही हे मला माहित आहे. संस्थेकडील ज्या कंत्राटामध्ये मी कामवर असेल ते कंत्राट बंद झाल्यास व दुसऱ्या ठिकाणी जागा रिकामी नसल्यास मला नोकरी वरून काढले जाईल हे मला मान्य आहे.",
        "९) ड्युटीवर असताना झोपेत सापडल्यास ५००/- दंड बसेल.",
        "१०) कंपनीने दिलेले हे सर्व नियम मला मान्य आहेत.",
    ]

    for rule in enumerate(dummy_rules):
        elements.append(Paragraph(f"{rule[1]}", custom_style))
        elements.append(Spacer(1, 6))

    # Fingerprints
    elements.append(Paragraph("<b>Left Finger</b>", styles['Heading3']))
    elements.append(Spacer(1, 6))

    left_finger_data = [["" for _ in range(5)]]
    left_finger_table = Table(left_finger_data, colWidths=[1*inch]*5, rowHeights=[1*inch])
    left_finger_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(left_finger_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Right Finger</b>", styles['Heading3']))
    elements.append(Spacer(1, 6))

    right_finger_data = [["" for _ in range(5)]]
    right_finger_table = Table(right_finger_data, colWidths=[1*inch]*5, rowHeights=[1*inch])
    right_finger_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(right_finger_table)
    elements.append(Spacer(1, 72))

    # Signature section
    signature_table_data = [
        [
            Paragraph("<b>Date:</b> ___________________", styles['Normal']),
            Paragraph("<b>Signature:</b> ___________________", styles['Normal']),
        ]
    ]
    signature_table = Table(signature_table_data, colWidths=[200, 200])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0, 'white'),
    ]))

    elements.append(signature_table)

    # Build PDF
    doc.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()

    return pdf_value


@login_required
def create_quotation(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        sr_no_list = request.POST.getlist('sr_no[]')
        description_list = request.POST.getlist('description[]')
        price_list = request.POST.getlist('price[]')

        # Generate the PDF
        pdf_buffer = generate_quotation_pdf(company_name, sr_no_list, description_list, price_list)

        # Return PDF as response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="quotation.pdf"'
        return response
    else:
        return render(request, 'FO/create_quotation.html')
    

from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_quotation_pdf(company_name, sr_no_list, description_list, price_list):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%d-%m-%Y")


    # Paths to images
    top_image_path = finders.find('imgs/letter_top.png')  # Path to the top image
    bottom_image_path = finders.find('imgs/letter_end.png')  # Path to the bottom image

    if not top_image_path or not bottom_image_path:
        raise FileNotFoundError("One or both image files were not found.")

    # Image dimensions
    top_image_height = 100  # Adjust the height as needed
    bottom_image_height = 50  # Adjust the height as needed

    # Draw the top image
    p.drawImage(top_image_path, 0, height - top_image_height, width=width, height=top_image_height)

    # Draw the bottom image
    p.drawImage(bottom_image_path, 0, 0, width=width, height=bottom_image_height)

    # Define margins for content
    top_margin = top_image_height + 10  # Space below the top image
    bottom_margin = bottom_image_height + 10  # Space above the bottom image

    # Define available content height
    content_start_y = height - top_margin
    content_end_y = bottom_margin

    # Set up fonts
    p.setFont("Times-Roman", 12)

    # Add company name
    p.drawString(100, content_start_y - 30, f"To: {company_name}")

    # Add subject
    p.drawString(100, content_start_y - 50, "Subject: Quotation for Security Guards")
    p.saveState()
    watermark = finders.find('imgs/logo.png')
    p.setFillAlpha(0.15)  # Set transparency level
    p.drawImage(str(watermark), width / 4, height / 4, width=width / 2, height=height / 2, mask='auto')
    p.restoreState()

    # Add salutation
    p.drawString(100, content_start_y - 70, "Dear Sir/Madam,")

    # Add introduction paragraph with manual line breaks
    intro_lines = [
        "                   We are pleased to submit our quotation for providing Security Supervisor,",
        "Housekeeping and Security Guards to your esteemed organization. We are committed",
        "to delivering services of the highest quality and we are looking formard to the overall",
        "success of your operations.We look forward to establishing a long-term partnership ",
        "with you. "
    ]

    line_height = 14  # Adjust line height if needed
    for i, line in enumerate(intro_lines):
        p.drawString(100, content_start_y - 110 - i * line_height, line)

    p.drawString(100, content_start_y - 200, "Below is the quotation for Security Services")
    # Draw the table
    table_start_y = content_start_y - 210  # Adjusted to make space for the paragraph
    col_widths = [50, 250, 120]  # Adjust the column widths
    row_height = 20

    # Create a grid for the table headers
    table_x = 90
    p.grid([table_x, table_x + col_widths[0], table_x + col_widths[0] + col_widths[1], 
            table_x + col_widths[0] + col_widths[1] + col_widths[2]], 
           [table_start_y, table_start_y - row_height])

    # Add headers
    p.drawString(table_x + 10, table_start_y - row_height + 5, "Sr. No.")
    p.drawString(table_x + col_widths[0] + 10, table_start_y - row_height + 5, "Description")
    p.drawString(table_x + col_widths[0] + col_widths[1] + 10, table_start_y - row_height + 5, "30/31 Days")

    # Draw the table content with grid
    table_y = table_start_y - row_height
    for sr_no, description, price in zip(sr_no_list, description_list, price_list):
        table_y -= row_height

        # Create a grid for each row
        p.grid([table_x, table_x + col_widths[0], table_x + col_widths[0] + col_widths[1], 
                table_x + col_widths[0] + col_widths[1] + col_widths[2]], 
               [table_y, table_y + row_height])

        # Add content
        p.drawString(table_x + 10, table_y + 5, str(sr_no))
        p.drawString(table_x + col_widths[0] + 10, table_y + 5, description)
        try:
            price = float(price)
        except ValueError:
            price = 0.0  # Handle invalid price formats gracefully
        p.drawString(table_x + col_widths[0] + col_widths[1] + 10, table_y + 5, f"Rs. {price:.2f} (12 Hrs)")
    # Add GST notice
    gst_notice = "18% GST will be applicable on overall billing."
    p.drawString(100, table_y - 20, gst_notice)

    # Add thank you note
    thank_you_note = "Thank you,"
    p.drawString(width - 100 - 100, bottom_margin + 300, thank_you_note)  # Align right
    company = "Best Security"
    p.drawString(width - 100 - 100, bottom_margin + 280, company) 
    p.drawString(width - 100 - 40, bottom_margin + 660, f"Date: {formatted_date}") 

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer




@login_required
def createquotation(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        sr_no_list = request.POST.getlist('sr_no[]')
        description_list = request.POST.getlist('description[]')
        price_list = request.POST.getlist('price[]')

        # Generate the PDF
        pdf_buffer = generate_quotation_pdf(company_name, sr_no_list, description_list, price_list)

        # Return PDF as response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="quotation.pdf"'
        return response
    else:
        return render(request, 'admin/createquotation.html')
    

from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_quotation_pdf(company_name, sr_no_list, description_list, price_list):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%d-%m-%Y")


    # Paths to images
    top_image_path = finders.find('imgs/letter_top.png')  # Path to the top image
    bottom_image_path = finders.find('imgs/letter_end.png')  # Path to the bottom image

    if not top_image_path or not bottom_image_path:
        raise FileNotFoundError("One or both image files were not found.")

    # Image dimensions
    top_image_height = 100  # Adjust the height as needed
    bottom_image_height = 50  # Adjust the height as needed

    # Draw the top image
    p.drawImage(top_image_path, 0, height - top_image_height, width=width, height=top_image_height)

    # Draw the bottom image
    p.drawImage(bottom_image_path, 0, 0, width=width, height=bottom_image_height)

    # Define margins for content
    top_margin = top_image_height + 10  # Space below the top image
    bottom_margin = bottom_image_height + 10  # Space above the bottom image

    # Define available content height
    content_start_y = height - top_margin
    content_end_y = bottom_margin

    # Set up fonts
    p.setFont("Times-Roman", 12)

    # Add company name
    p.drawString(100, content_start_y - 30, f"To: {company_name}")

    # Add subject
    p.drawString(100, content_start_y - 50, "Subject: Quotation for Security Guards")

    # Add salutation
    p.drawString(100, content_start_y - 70, "Dear Sir/Madam,")

    # Add introduction paragraph with manual line breaks
    intro_lines = [
        "                   We are pleased to submit our quotation for providing Security Supervisor,",
        "Housekeeping and Security Guards to your esteemed organization. We are committed",
        "to delivering services of the highest quality and we are looking formard to the overall",
        "success of your operations.We look forward to establishing a long-term partnership ",
        "with you. "
    ]

    line_height = 14  # Adjust line height if needed
    for i, line in enumerate(intro_lines):
        p.drawString(100, content_start_y - 110 - i * line_height, line)

    p.drawString(100, content_start_y - 200, "Below is the quotation for Security Services")
    # Draw the table
    table_start_y = content_start_y - 210  # Adjusted to make space for the paragraph
    col_widths = [50, 250, 120]  # Adjust the column widths
    row_height = 20

    # Create a grid for the table headers
    table_x = 90
    p.grid([table_x, table_x + col_widths[0], table_x + col_widths[0] + col_widths[1], 
            table_x + col_widths[0] + col_widths[1] + col_widths[2]], 
           [table_start_y, table_start_y - row_height])

    # Add headers
    p.drawString(table_x + 10, table_start_y - row_height + 5, "Sr. No.")
    p.drawString(table_x + col_widths[0] + 10, table_start_y - row_height + 5, "Description")
    p.drawString(table_x + col_widths[0] + col_widths[1] + 10, table_start_y - row_height + 5, "30/31 Days")

    # Draw the table content with grid
    table_y = table_start_y - row_height
    for sr_no, description, price in zip(sr_no_list, description_list, price_list):
        table_y -= row_height

        # Create a grid for each row
        p.grid([table_x, table_x + col_widths[0], table_x + col_widths[0] + col_widths[1], 
                table_x + col_widths[0] + col_widths[1] + col_widths[2]], 
               [table_y, table_y + row_height])

        # Add content
        p.drawString(table_x + 10, table_y + 5, str(sr_no))
        p.drawString(table_x + col_widths[0] + 10, table_y + 5, description)
        try:
            price = float(price)
        except ValueError:
            price = 0.0  # Handle invalid price formats gracefully
        p.drawString(table_x + col_widths[0] + col_widths[1] + 10, table_y + 5, f"Rs. {price:.2f} (12 Hrs)")
    # Add GST notice
    gst_notice = "18% GST will be applicable on overall billing."
    p.drawString(100, table_y - 20, gst_notice)

    # Add thank you note
    thank_you_note = "Thank you,"
    p.drawString(width - 100 - 100, bottom_margin + 300, thank_you_note)  # Align right
    company = "Best Security"
    p.drawString(width - 100 - 100, bottom_margin + 280, company) 
    p.drawString(width - 100 - 40, bottom_margin + 660, f"Date: {formatted_date}") 

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer



############################################# FO Attendance ########################################################### 
# def addshift(request):
#     if request.method == 'POST':
#         intime = request.POST.get('intime')
#         outtime = request.POST.get('outtime')
#         description = request.POST.get('description')

#         # Convert intime and outtime to datetime objects
#         intime_dt = datetime.strptime(intime, '%H:%M')
#         outtime_dt = datetime.strptime(outtime, '%H:%M')

#         # Calculate total time in hours
#         time_difference = outtime_dt - intime_dt
#         shift_total_time = abs(time_difference.total_seconds()) / 3600

#         # Create a new ShiftTime object and save it to the database
#         ShiftTime.objects.create(
#             intime=intime,
#             outtime=outtime,
#             description=description,
#             shift_total_time=shift_total_time
#         )

#         return redirect('shift_list')  # Redirect to the shift list page after saving

#     return render(request, 'FO/addshift.html')

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ShiftTime
from datetime import datetime

def addshift(request):
    if request.method == 'POST':
        try:
            intime = request.POST.get('intime')
            outtime = request.POST.get('outtime')
            description = request.POST.get('description')

            # Convert intime and outtime to datetime objects
            intime_dt = datetime.strptime(intime, '%H:%M')
            outtime_dt = datetime.strptime(outtime, '%H:%M')

            # Calculate total time in hours
            time_difference = outtime_dt - intime_dt
            shift_total_time = abs(time_difference.total_seconds()) / 3600

            # Create a new ShiftTime object and save it to the database
            ShiftTime.objects.create(
                intime=intime,
                outtime=outtime,
                description=description,
                shift_total_time=shift_total_time
            )

            # Return success response
            return JsonResponse({'success': True})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Handle GET request by rendering the form
    return render(request, 'FO/addshift.html')


def shift_list(request):
    shifts = ShiftTime.objects.all()
    return render(request, 'FO/shift_list.html', {'shifts': shifts})

def fo_attendance(request):
    return render(request,'FO/markattendance.html')
#############################################################################################


def markattendance(request):
    if request.method == 'GET':
        employees = EmployeeJoining.objects.all()
        companies = UserProfile.objects.filter(user_type='company')
        return render(request, 'FO/markattendance.html', {'employees': employees, 'companies': companies})




# @require_POST
# def submit_attendance(request, employee_id):
#     date = request.POST.get('date')
#     status = request.POST.get('status')
#     shift_id = request.POST.get('shift')
#     notes = request.POST.get('notes')

#     # Validate date and status
#     if not date:
#         return JsonResponse({'error': 'Date is required'}, status=400)
#     if not status:
#         return JsonResponse({'error': 'Status is required'}, status=400)

#     try:
#         employee = get_object_or_404(EmployeeJoining, id=employee_id)
#         shift = get_object_or_404(ShiftTime, id=shift_id) if shift_id else None

#         # Set check_in_time and check_out_time based on shift
#         check_in_time = shift.intime if shift else None
#         check_out_time = shift.outtime if shift else None

#         # Create or update attendance
#         attendance, created = Attendance.objects.update_or_create(
#             employee=employee,
#             date=date,
#             defaults={
#                 'status': status,
#                 'check_in_time': check_in_time,
#                 'check_out_time': check_out_time,
#                 'shift': shift,
#                 'notes': notes
#             }
#         )
        
#         return JsonResponse({'message': 'Attendance updated successfully'})

#     except EmployeeJoining.DoesNotExist:
#         return JsonResponse({'error': 'Employee not found'}, status=404)
#     except ShiftTime.DoesNotExist:
#         return JsonResponse({'error': 'Shift not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

@require_POST
def submit_attendance(request, employee_id):
    date = request.POST.get('date')
    status = request.POST.get('status')
    shift_id = request.POST.get('shift')
    notes = request.POST.get('notes')

    if not date or not status:
        return redirect(f"{request.META.get('HTTP_REFERER')}?error=Date and status are required.")

    try:
        employee = get_object_or_404(EmployeeJoining, id=employee_id)
        shift = get_object_or_404(ShiftTime, id=shift_id)

        check_in_time = shift.intime if shift else None
        check_out_time = shift.outtime if shift else None

        attendance, created = Attendance.objects.update_or_create(
            employee=employee,
            date=date,
            defaults={
                'status': status,
                'check_in_time': check_in_time,
                'check_out_time': check_out_time,
                'shift': shift,
                'notes': notes
            }
        )

        return redirect(f"{request.META.get('HTTP_REFERER')}?success=true")

    except EmployeeJoining.DoesNotExist:
        return redirect(f"{request.META.get('HTTP_REFERER')}?error=Employee not found.")
    except ShiftTime.DoesNotExist:
        return redirect(f"{request.META.get('HTTP_REFERER')}?error=Shift not found.")
    except Exception as e:
        return redirect(f"{request.META.get('HTTP_REFERER')}?error={str(e)}")

