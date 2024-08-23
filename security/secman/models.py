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
    emergency_contact_relation1_address = models.CharField(max_length=100)
    emergency_contact_relation2_address = models.CharField(max_length=100)
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
    advance_payment = models.IntegerField()
    food_allowance = models.IntegerField()

    def __str__(self):
        return f"Salary Details for {self.user.username}"
