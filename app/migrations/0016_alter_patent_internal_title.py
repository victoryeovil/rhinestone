# Generated by Django 4.2.4 on 2023-08-27 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_agent_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patent',
            name='internal_title',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Internal Title'),
        ),
    ]
