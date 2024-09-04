from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta

from django.utils import timezone

from decimal import Decimal
class UserProfile(models.Model):
    USER_TYPES = (
        ('hod', 'HOD'),
        ('fo', 'Field Officer'),
        ('company', 'Company'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='fo')
    contact = models.CharField(max_length=12)
    gst_or_emergency = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.email} ({self.get_user_type_display()})"
    

##############################Shubham##############################

class BirthdayCompany(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    description = models.TextField()
    birthday_date = models.DateField()


# class EmployeeJoining(models.Model):
#     emp_id = models.CharField(max_length=20, unique=True)
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50, blank=True, null=True)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     date_of_birth = models.DateField()
#     contact_number = models.CharField(max_length=15)
#     whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
#     emergency_contact1 = models.CharField(max_length=15)
#     emergency_contact2 = models.CharField(max_length=15)
#     emergency_contact_relation1 = models.CharField(max_length=20)
#     emergency_contact_relation2 = models.CharField(max_length=20)
#     emergency_contact_relation1_address = models.CharField(max_length=100)
#     emergency_contact_relation2_address = models.CharField(max_length=100)
#     age = models.PositiveIntegerField()
#     gender = models.CharField(max_length=10)
#     current_address = models.TextField()
#     permanent_address = models.TextField()
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     pincode = models.CharField(max_length=10)
#     security_guard_training = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
#     job_experience = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
#     pancard = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
#     aadhar = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
#     voter = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
#     profile_picture = models.ImageField(upload_to='profile_pictures/')
#     signature = models.ImageField(upload_to='signatures/')
#     preferred_work_arrangements = models.CharField(max_length=20)
#     position = models.CharField(max_length=50)
#     account_holder_name = models.CharField(max_length=100)
#     bank_name = models.CharField(max_length=100)
#     bank_account_number = models.CharField(max_length=30)
#     ifsc_code = models.CharField(max_length=15)
#     branch_name = models.CharField(max_length=100)
#     bank_address = models.TextField()
#     qualification = models.CharField(max_length=20)
#     experience = models.CharField(max_length=20)
#     company = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'company'})
    
#     shift = models.ForeignKey('ShiftTime', on_delete=models.SET_NULL, null=True)
#     pdf_file = models.FileField(upload_to='employee_pdfs/', blank=True, null=True)

    

#     def __str__(self):
#         return self.emp_id
class EmployeeJoining(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact1 = models.CharField(max_length=15)
    emergency_contact2 = models.CharField(max_length=15)
    emergency_contact_relation1 = models.CharField(max_length=20)
    emergency_contact_relation2 = models.CharField(max_length=20)
    emergency_contact_relation1_name = models.CharField(max_length=100)
    emergency_contact_relation2_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    current_address = models.TextField()
    permanent_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    security_guard_training = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    job_experience = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    pancard = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    aadhar = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    voter = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    signature = models.ImageField(upload_to='signatures/')
    preferred_work_arrangements = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=15)
    branch_name = models.CharField(max_length=100)
    bank_address = models.TextField()
    qualification = models.CharField(max_length=20)
    experience = models.CharField(max_length=20)
    company = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'company'})
    
    pdf_file = models.FileField(upload_to='employee_pdfs/', blank=True, null=True)
    # joining_date = models.DateField()
    
    

    def __str__(self):
        return self.emp_id
    
    
class ShiftTime(models.Model):
    intime = models.TimeField()
    outtime = models.TimeField()
    description = models.CharField(max_length=255)
    shift_total_time = models.FloatField(editable=False)  # Store the total time in hours

    

    def __str__(self):
        return f"{self.description} ({self.intime} - {self.outtime})"
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
        ('H', 'Holiday'),
    ]

    employee = models.ForeignKey(EmployeeJoining, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    shift = models.ForeignKey(ShiftTime, on_delete=models.SET_NULL, null=True)  # Link to ShiftTime model
    notes = models.TextField(blank=True, null=True)  # Optional field to add any notes or remarks

    def __str__(self):
        return f"{self.employee.emp_id} - {self.date} - {self.shift.description}"

    class Meta:
        unique_together = ('employee', 'date')  # Ensure that an employee cannot have duplicate attendance records on the same day
        ordering = ['date']
        





    










class Quotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    sr_no = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='quotations/', null=True, blank=True)

    def __str__(self):
        return f"Quotation for {self.company.user.email} by {self.user.email}"


class Quotations(models.Model):
    # Fields for security guards
    company = models.CharField(max_length=100)
    guard_basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    guard_special_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    guard_total_a = models.DecimalField(max_digits=10, decimal_places=2)
    guard_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    guard_education_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    guard_travelling_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    guard_house_duty = models.DecimalField(max_digits=10, decimal_places=2)
    guard_total_b = models.DecimalField(max_digits=10, decimal_places=2)
    guard_washing_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    guard_hra = models.DecimalField(max_digits=10, decimal_places=2)
    guard_sub_total_c = models.DecimalField(max_digits=10, decimal_places=2)
    guard_pf = models.DecimalField(max_digits=10, decimal_places=2)
    guard_gratuity = models.DecimalField(max_digits=10, decimal_places=2)
    guard_leave_with_wages = models.DecimalField(max_digits=10, decimal_places=2)
    guard_esic = models.DecimalField(max_digits=10, decimal_places=2)
    guard_paid_holiday = models.DecimalField(max_digits=10, decimal_places=2)
    guard_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    guard_uniform = models.DecimalField(max_digits=10, decimal_places=2)
    # guard_charges = models.DecimalField(max_digits=10, decimal_places=2)
    guard_total_c = models.DecimalField(max_digits=10, decimal_places=2)
    guard_service_charges = models.DecimalField(max_digits=10, decimal_places=2)
    guard_grand_total_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    # Fields for supervisors
    supervisor_basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_special_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_total_a = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_education_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_travelling_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_house_duty = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_total_b = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_washing_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_hra = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_sub_total_c = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_pf = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_gratuity = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_leave_with_wages = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_esic = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_paid_holiday = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_uniform = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_total_c = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_service_charges = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_grand_total_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    # Add additional fields if needed
    pdf_file = models.FileField(upload_to='quotations/', blank=True, null=True)



from django.db import models

class TaxInvoice(models.Model):
    company = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    month = models.CharField(max_length=15)
    year = models.PositiveIntegerField()
    guard_count = models.PositiveIntegerField()
    amount_per_guard = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor_count =models.DecimalField(max_digits=10, decimal_places=2)
    amount_per_supervisor =models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(max_digits=12,decimal_places=2)
    cgst = models.DecimalField(max_digits=12,decimal_places=2)
    sgst = models.DecimalField(max_digits=12,decimal_places=2)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)  # Add this line

    def __str__(self):
        return f"Tax Invoice for {self.company.user.username} - {self.total_amount}"
    
    
    
from django.db import models
from django.contrib.auth.models import User

class SalaryDetails(models.Model):
    employee = models.ForeignKey(EmployeeJoining, on_delete=models.CASCADE) 
    basic_salary = models.IntegerField()
    special_allowance = models.IntegerField()
    total = models.IntegerField()
    conveyance_allowance = models.IntegerField()
    education_allowance = models.IntegerField()
    travelling_allowance = models.IntegerField()
    hours_daily_duty = models.IntegerField()
    total_b = models.IntegerField()
    hra = models.IntegerField()
    pf = models.IntegerField()
    gratuity = models.IntegerField()
    leave_with_wages = models.IntegerField()
    esic = models.IntegerField()
    paid_holiday = models.IntegerField()
    bonus = models.IntegerField()
    uniform = models.IntegerField()
    total_c = models.IntegerField()
    service_charge = models.IntegerField()
    food_allowance = models.IntegerField()
    price_partial_uniform = models.IntegerField()
    
    
    advance_payment = models.IntegerField(null=True, blank=True)
    advance_request_status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending'
    )
    advance_payment_approval_date = models.DateTimeField(blank=True, null=True)
    
    actual_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    
    
    
    
    replicated_basic_salary = models.IntegerField()
    replicated_special_allowance = models.IntegerField()
    replicated_conveyance_allowance = models.IntegerField()
    replicated_education_allowance = models.IntegerField()
    replicated_travelling_allowance = models.IntegerField()
    replicated_hours_daily_duty = models.IntegerField()
    
    replicated_food_allowance = models.IntegerField()
    replicated_service_charge = models.IntegerField()

    # Additional replicated fields for calculated values
    replicated_total = models.IntegerField()
    replicated_total_b = models.IntegerField()
    replicated_hra = models.IntegerField()
    replicated_pf = models.IntegerField()
    replicated_gratuity = models.IntegerField()
    replicated_leave_with_wages = models.IntegerField()
    replicated_esic = models.IntegerField()
    replicated_paid_holiday = models.IntegerField()
    replicated_bonus = models.IntegerField()
    replicated_total_c = models.IntegerField()
    replicated_actual_salary = models.IntegerField()
    
    
    
    def __str__(self):
        return f"Salary Details for {self.user.username}"
    
    
    



