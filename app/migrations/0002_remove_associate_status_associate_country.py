# Generated by Django 4.2.4 on 2024-07-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associate',
            name='status',
        ),
        migrations.AddField(
            model_name='associate',
            name='country',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Country/State'),
        ),
    ]
