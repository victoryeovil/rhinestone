# Generated by Django 4.2.4 on 2024-11-05 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_inventiondisclosure_approved_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='id_ref_number',
            field=models.CharField(blank=True, max_length=10, unique=True, verbose_name='ID Reference'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='cost_centre',
            field=models.ForeignKey(blank=True, max_length=128, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cost_center', to='app.costcenter', verbose_name='Cost Centre'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='cost_centre_code',
            field=models.ForeignKey(blank=True, max_length=128, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.costcenter', verbose_name='Cost Centre Code'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='country',
            field=models.CharField(blank=True, choices=[('AU', 'AU: Australia'), ('CA', 'CA: Canada'), ('FR', 'FR: France'), ('DE', 'DE: Germany'), ('IE', 'IE: Ireland'), ('IT', 'IT: Italy'), ('JP', 'JP: Japan'), ('KP', "KP: Korea, Democratic People's Republic of"), ('NO', 'NO: Norway'), ('RU', 'RU: Russia'), ('ZA', 'ZA: South Africa'), ('TW', 'TW: Taiwan'), ('UA', 'UA: Ukraine'), ('GB', 'GB: United Kingdom'), ('USA', 'USA: United States of America'), ('VA', 'VA: Vatican City (Holy See)')], max_length=128, null=True, verbose_name='Country'),
        ),
    ]
