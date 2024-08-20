# Generated by Django 5.0.7 on 2024-08-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secman', '0005_employeejoining_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeejoining',
            name='basic_salary',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='conveyance_allowance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='education_allowance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='esic',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='gratuity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='hours_daily_duty',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='hra',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='leave_with_wages',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='paid_holiday',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='pf',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='service_charge',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='special_allowance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='total_b',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='total_c',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='travelling_allowance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeejoining',
            name='uniform',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]