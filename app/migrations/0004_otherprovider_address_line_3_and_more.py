# Generated by Django 4.2.4 on 2024-07-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_associate_country_alter_contact_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherprovider',
            name='address_line_3',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Address Line 3'),
        ),
        migrations.AddField(
            model_name='otherprovider',
            name='country_states',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='County/State'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='MID',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='inventor',
            name='type_of_contract',
            field=models.CharField(blank=True, choices=[('Employee', 'Employee'), ('Contractor', 'Contractor'), ('Secondment', 'Secondment'), ('Licensor', 'Licensor')], max_length=12, null=True),
        ),
    ]