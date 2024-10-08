# Generated by Django 4.2.4 on 2024-10-02 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_inventiondisclosure_cost_centre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventiondisclosure',
            name='Paralegal 1',
        ),
        migrations.RemoveField(
            model_name='inventiondisclosure',
            name='Paralegal 2',
        ),
        migrations.RemoveField(
            model_name='inventiondisclosure',
            name='Reference ID',
        ),
        migrations.AddField(
            model_name='inventiondisclosure',
            name='id_ref_number',
            field=models.CharField(blank=True, max_length=10, unique=True, verbose_name='Reference ID'),
        ),
        migrations.AddField(
            model_name='inventiondisclosure',
            name='primary_paralegal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_paralegal_set', to='app.paralegal', verbose_name='Primary Paralegal'),
        ),
        migrations.AddField(
            model_name='inventiondisclosure',
            name='secondary_paralegal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_paralegal_set', to='app.paralegal', verbose_name='Secondary Paralegal'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='agreement',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Agreement'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='approval_or_rejection_date',
            field=models.DateField(blank=True, null=True, verbose_name='Approval or Rejection Date'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='approved_by',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Approved By'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='approved_for_filing',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Approved for Filing'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='attorney_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attorney_1_set', to='app.attorney', verbose_name='Attorney 1'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='attorney_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attorney_2_set', to='app.attorney', verbose_name='Attorney 2'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='confirmed_inventors',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Confirmed Inventors'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='cost_centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invention_cost_centre', to='app.costcenter', verbose_name='Cost Centre'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='cost_centre_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invention_cost_centre_code', to='app.costcenter', verbose_name='Cost Centre Code'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='date_file_opened',
            field=models.DateField(blank=True, null=True, verbose_name='Date File Opened'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='date_of_invention',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Invention'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='files',
            field=models.ManyToManyField(to='app.file', verbose_name='Attached Files'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='general_notes',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='General Notes'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='invention_description',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Invention Description'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='joint_venture',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Joint Venture'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='keyword',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Keyword(s)'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='proposed_inventors',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Proposed Inventors'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='reasons_of_approval_or_rejection',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Reasons of Approval or Rejection'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='status',
            field=models.CharField(choices=[('OPENED', 'OPENED'), ('PENDING', 'PENDING'), ('UNDER REVIEW', 'UNDER REVIEW'), ('PROCESSED', 'PROCESSED'), ('NOT PROCESSED', 'NOT PROCESSED'), ('ABANDONED', 'ABANDONED'), ('SOLD', 'SOLD')], max_length=64, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='inventiondisclosure',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title'),
        ),
    ]
