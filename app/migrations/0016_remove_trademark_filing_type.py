# Generated by Django 4.2.4 on 2024-09-05 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_attorney_case_office_design_filing_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trademark',
            name='filing_type',
        ),
    ]
