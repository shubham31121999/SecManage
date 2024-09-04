from celery import shared_task
from .models import SalaryDetails, Attendance
from datetime import datetime

@shared_task
def update_salary_details_based_on_attendance():
    today = datetime.now().date()
    
    salary_details = SalaryDetails.objects.all()
    for salary in salary_details:
        # Assuming that attendance is stored on a daily basis
        attendance = Attendance.objects.filter(employee=salary.employee, date=today).first()
        
        if attendance and attendance.status == 'P':  # Assuming 'P' stands for 'Present'
            # Replicating fields based on attendance
            salary.replicated_basic_salary = salary.basic_salary
            salary.replicated_special_allowance = salary.special_allowance
            salary.replicated_conveyance_allowance = salary.conveyance_allowance
            salary.replicated_education_allowance = salary.education_allowance
            salary.replicated_travelling_allowance = salary.travelling_allowance
            salary.replicated_hours_daily_duty = salary.hours_daily_duty
            salary.replicated_food_allowance = salary.food_allowance
            salary.replicated_service_charge = salary.service_charge

            # Calculating additional replicated fields
            salary.replicated_total = salary.replicated_basic_salary + salary.replicated_special_allowance
            salary.replicated_total_b = (salary.replicated_conveyance_allowance + 
                                         salary.replicated_education_allowance + 
                                         salary.replicated_travelling_allowance)
            salary.replicated_hra = int(0.05 * salary.replicated_total)  # Assuming HRA is 5% of the total
            salary.replicated_pf = int(0.13 * salary.replicated_total)   # Assuming PF is 13% of the total
            salary.replicated_gratuity = salary.gratuity
            salary.replicated_leave_with_wages = salary.leave_with_wages
            salary.replicated_esic = salary.esic
            salary.replicated_paid_holiday = salary.paid_holiday
            salary.replicated_bonus = salary.bonus
            salary.replicated_total_c = salary.replicated_total_b + salary.replicated_hra + salary.replicated_pf
            salary.replicated_actual_salary = (salary.replicated_total + 
                                               salary.replicated_total_b + 
                                               salary.replicated_total_c - 
                                               salary.advance_payment)

            # Save the updated salary details
            salary.save()
        else:
            # Handle cases where the employee was absent or other statuses
            pass
