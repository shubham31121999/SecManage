# Generated by Django 5.0.7 on 2024-08-12 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secman', '0003_employeejoining'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeejoining',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='employee_pdfs/'),
        ),
    ]