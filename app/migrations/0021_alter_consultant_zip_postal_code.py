# Generated by Django 4.2.4 on 2024-04-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_family_applicant_alter_family_inventor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='zip_postal_code',
            field=models.CharField(blank=True, default=1, max_length=12, verbose_name='Zip/Postal Code'),
            preserve_default=False,
        ),
    ]
