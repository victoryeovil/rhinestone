from typing import *
from django.db.models import Q
from django import forms
from django.core.files.base import File
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field, HTML,Div
from itertools import chain
from app import models
from app import data
from app.data.common import CASE_TYPE
from app.functions.chunk import chunk
from app.models import (
    Family, Patent, Trademark, Design, BaseModel,
    User, Contact, InventionDisclosure, Invoice
)
from app.models.contacts import Applicant, Associate, Attorney, CostCenter, Inventor, Paralegal


class QuickSearchForm(forms.Form):
    _official_numbers__icontains = forms.CharField(required=False, label="Official Number")
    _titles__icontains = forms.CharField(required=False, label="Title")
    primary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
    secondary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
    type_of_filing = forms.ChoiceField(required=False, choices=data.common.BLANK_OPTIONS + [(i, i) for i in ["Trademark", "Design", "Patent"]])
    _Associates = forms.ModelChoiceField(
        models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
        required=False
    )
    _Associate_refs = forms.ModelChoiceField(
        models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
        required=False
    )
    status__in = forms.MultipleChoiceField(required=False, label="Status", choices=data.common.BLANK_OPTIONS + [(i, i) for i in ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired", "Published"]])
    query = forms.CharField(required=False, label="Search Query")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("_official_numbers__icontains", css_class="col-12 col-md-6"),
                Column("_titles__icontains", css_class="col-12 col-md-6"),
                Column("primary_attorney", css_class="col-12 col-md-6"),
                Column("secondary_attorney", css_class="col-12 col-md-6"),
                Column("type_of_filing", css_class="col-12 col-md-6"),
                Column("status__in", css_class="col-12 col-md-6"),
                Column("_Associates", css_class="col-12 col-md-6"),
                Column("_Associate_refs", css_class="col-12 col-md-6"),
                Column("query", css_class="col-12")
            ),
            Row(
                Column(
                    HTML("""
                        <a class="btn btn-secondary mx-3" href="{{ request.path }}">
                            <i class="feather icon-minus"></i>&nbsp;Clear
                        </a>
                        <button class="btn btn-primary mx-3" type="submit">
                            <i class="feather icon-search"></i>&nbsp;Search
                        </button>
                    """),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('query')

        if not any(cleaned_data.values()) and not query:
            raise forms.ValidationError("Please enter at least one search criterion")

        if query:
            # Perform the search across multiple models
            patent_results = Patent.objects.filter(Q(_titles__icontains=query) | Q(official_numbers__icontains=query))
            trademark_results = Trademark.objects.filter(titles__icontains=query)
            family_results = Family.objects.filter(titles__icontains=query)
            design_results = Design.objects.filter(titles__icontains=query)

            results = list(chain(patent_results, trademark_results, family_results, design_results))

            if not results:
                raise forms.ValidationError("Search not found")

            cleaned_data['results'] = results

        return cleaned_data
    


# class HomeSearchForm(forms.Form):
#     _official_numbers__icontains = forms.CharField(required=False, label="Official Number")
#     official = _official_numbers__icontains
#     _titles__icontains = forms.CharField(required=False, label="Title")
#     titles = _titles__icontains
#     primary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
#     secondary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
#     type_of_filing = forms.ChoiceField(required=False, choices=[("","")] + [(i, i) for i in ["Trademark", "Design", "Patent"]])
#     _Associates = forms.ModelChoiceField(
#         models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
#         required=False
#     )
#     _Associate_refs = forms.ModelChoiceField(
#         models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
#         required=False
#     )
#     status__in = forms.MultipleChoiceField(required=False, label="Status", choices=[("","")] + [(i, i) for i in ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired", "Published"]])
#     query = forms.CharField(required=False, label="Search Query")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column("_official_numbers__icontains", css_class="col-12 col-md-6"),
#                 Column("_titles__icontains", css_class="col-12 col-md-6"),
#                 Column("primary_attorney", css_class="col-12 col-md-6"),
#                 Column("secondary_attorney", css_class="col-12 col-md-6"),
#                 Column("type_of_filing", css_class="col-12 col-md-6"),
#                 Column("status__in", css_class="col-12 col-md-6"),
#                 Column("_Associates", css_class="col-12 col-md-6"),
#                 Column("_Associate_refs", css_class="col-12 col-md-6"),
#                 #Column("query", css_class="col-12")
#             ),
#             Row(
#                 Column(
#                     HTML("""
#                         <a class="btn btn-secondary mx-3" href="{{ request.path }}">
#                             <i class="feather icon-minus"></i>&nbsp;Clear
#                         </a>
#                         <button class="btn btn-primary mx-3" type="submit">
#                             <i class="feather icon-search"></i>&nbsp;Search
#                         </button>
#                     """),
#                     css_class="col-12 pt-3 text-center"
#                 )
#             )
#         )

class HomeSearchForm(forms.Form):
    # Name Section
    associate = forms.ModelChoiceField(queryset=Associate.objects.all(), required=False, label="Agent/Associates")
    instructor = forms.ModelChoiceField(queryset=Contact.objects.filter(type__in=["Associate", "Client"]), required=False, label="Instructor")
    owner = forms.ModelChoiceField(queryset=Applicant.objects.all(), required=False, label="Owner")
    name = forms.ModelChoiceField(queryset=Contact.objects.all(), required=False, label="Name")
    name_type = forms.ChoiceField(choices=[
        ('', '---'),  # Empty value for Name Type
        ('Inventor', 'Inventor'),
        ('Applicant', 'Applicant'),
        ('Licensor', 'Licensor'),
        ('Licensee', 'Licensee'),
        ('Consultant', 'Consultant'),
        ('Associate', 'Associate'),
        ('Paralegal', 'Paralegal'),
        ('Attorney', 'Attorney'),
        ('OtherProvider', 'OtherProvider')
    ], required=False, label="Name Type")

    # Primary and Secondary Attorney fields
    primary_attorney = forms.ModelChoiceField(queryset=Attorney.objects.all(), required=False, label="Primary Attorney")
    secondary_attorney = forms.ModelChoiceField(queryset=Attorney.objects.all(), required=False, label="Secondary Attorney")

    # New fields for Names Section
    primary_paralegal = forms.ModelChoiceField(queryset=Paralegal.objects.all(), required=False, label="Primary Paralegal")
    secondary_paralegal = forms.ModelChoiceField(queryset=Paralegal.objects.all(), required=False, label="Secondary Paralegal")
    inventor = forms.ModelChoiceField(queryset=Inventor.objects.all(), required=False, label="Inventor")

    # References Section
    case_reference = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Case Reference")
    family = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Family")
    official_number = forms.CharField(required=False, label="Official Number")
    cost_centre = forms.ModelChoiceField(queryset=CostCenter.objects.all(), required=False, label="Cost Center")
    instructor_reference = forms.ModelChoiceField(queryset=Family.objects.values_list('licensor', flat=True).distinct(), required=False, label="Instructor Reference")

    # Added Associate Refs
    Associate_refs = forms.ModelChoiceField(queryset=Associate.objects.all(), required=False, label="Associate Refs")

    # All Numbers under References
    priority_provisional_application_no = forms.CharField(required=False, label="Priority/Provisional Application No")
    pct_application_no = forms.CharField(required=False, label="PCT Application No")
    application_no = forms.CharField(required=False, label="Application No")  # Consolidated field for national, design, and priority application numbers
    publication_no = forms.CharField(required=False, label="Publication No")
    grant_number = forms.CharField(required=False, label="Grant Number")
    registration_no = forms.CharField(required=False, label="Registration No")

    # Type of Filing Field
    type_of_filing = forms.ChoiceField(choices=[("", "---"), ("Trademark", "Trademark"), ("Design", "Design"), ("Patent", "Patent"), ("Copyright", "Copyright")], required=False, label="Property Type")

    # Case Details Section
    case_office = forms.CharField(required=False, label="Case Office")
    
    # Add an empty option to ensure '---' is selected by default
    case_type = forms.ChoiceField(choices=[('', '---')] + [(i, i) for i in CASE_TYPE], required=False, label="Filing Type")
    
    # Add an empty option to the country field
    country = forms.ChoiceField(choices=[('', '---')] + list(data.countries.COUNTRIES_OPTIONS), required=False, label="Country")
    
    property_type = forms.CharField(required=False, label="Property Type")
    #case_category = forms.CharField(required=False, label="Case Category")
    sub_type = forms.ChoiceField(choices=[('',"---"), ('PCT National Phase','PCT National Phase'),('Divisional', 'Divisional'), ('Non Provisional', 'Non Provisional'),
                                          ('Continuation', 'Continuation'), ('EP National', 'EP National'), ('EP-PECT National', 'EP-PECT National')],required=False, label="Sub Filing Type")
    basis = forms.CharField(required=False, label="Basis")
    case_class = forms.CharField(required=False, label="Class")
    
    # New Classes Field
    classes = forms.IntegerField(required=False, label="Classes")

    # Status Section (Checkboxes with additional options)
    status__in = forms.MultipleChoiceField(
        required=False,
        label="Status",
        choices=[
            ("Pending", "Pending"),
            ("Registered", "Registered"),
            ("Dead", "Dead"),
            ("Open", "Open"),
            ("Filed", "Filed"),
            ("Allowed", "Allowed"),
            ("Granted(Live)", "Granted(Live)"),
            ("Abandoned", "Abandoned"),
            ("Granted(DEAD)", "Granted(DEAD)"),
            ("Converted", "Converted"),
            ("Expired", "Expired"),
            ("Published", "Published"),
            ("Renewal overdue", "Renewal overdue"),
            ("Renewal not paid", "Renewal not paid"),
            ("Renewal expired", "Renewal expired"),
            ("Examination", "Examination")
        ],
        widget=forms.CheckboxSelectMultiple,
        help_text="Select multiple statuses. Choices are displayed in 5 columns."
    )
    

    case_status = forms.CharField(required=False, label="Case Status")
    renewal_status = forms.ChoiceField(choices=[('',"---"), ('Pending','Pending'),('Payment in Process', 'Payment in Process'), (' Renewals', 'Renewals'),
                                          ('Renewals Handled Elsewhere', 'Renewals Handled Elsewhere')],required=False, label="Renewal Status")

    # Text Section
    title = forms.CharField(required=False, label="Title")
    keyword = forms.CharField(required=False, label="Keyword")
    text_type = forms.ChoiceField(choices=[("Any", "Any")], required=False, label="Text Type")
    type_of_mark = forms.CharField(required=False, label="Type of Mark")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Names Section
            Div(
                Div(
                    Field('associate', css_class="form-control"),
                    Field('instructor', css_class="form-control"),
                    Field('owner', css_class="form-control"),
                    Field('name', css_class="form-control"),
                    Field('name_type', css_class="form-control"),
                    Field('primary_attorney', css_class="form-control"),  # Primary Attorney
                    Field('secondary_attorney', css_class="form-control"),  # Secondary Attorney
                    Field('primary_paralegal', css_class="form-control"),
                    Field('secondary_paralegal', css_class="form-control"),
                    Field('inventor', css_class="form-control"),
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # References Section
            Div(
                Div(
                    Field('case_reference', css_class="form-control"),
                    Field('family', css_class="form-control"),
                    Field('cost_centre',css_class="form-control"),
                    Field('official_number', css_class="form-control"),
                    Field('instructor_reference', css_class="form-control"),  # Added Instructor Reference
                    Field('Associate_refs', css_class="form-control"),  # Added Associate Refs
                    Field('priority_provisional_application_no', css_class="form-control"),
                    Field('pct_application_no', css_class="form-control"),
                    Field('application_no', css_class="form-control"),  # Consolidated application number field
                    Field('publication_no', css_class="form-control"),
                    Field('grant_number', css_class="form-control"),
                    Field('registration_no', css_class="form-control"),
                    Field('type_of_filing', css_class="form-control"),  # Added Type of Filing
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # Case Details Section
            Div(
                Div(
                    Field('case_office', css_class="form-control"),
                    Field('case_type', css_class="form-control"),
                    Field('country', css_class="form-control"),
                    Field('property_type', css_class="form-control"),
                    Field('case_category', css_class="form-control"),
                    Field('sub_type', css_class="form-control"),
                    Field('basis', css_class="form-control"),
                    Field('case_class', css_class="form-control"),
                    Field('classes', css_class="form-control"),
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # Status Section
            Div(
                Div(
                    Field('status__in', css_class="form-control"),
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # Text Section
            Div(
                Div(
                    Field('title', css_class="form-control"),
                    Field('keyword', css_class="form-control"),
                    Field('text_type', css_class="form-control"),
                    Field('type_of_mark', css_class="form-control"),
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # Buttons
            Row(
                Column(
                    HTML("""
                        <a class="btn btn-secondary mx-3" href="{{ request.path }}">
                            <i class="feather icon-minus"></i>&nbsp;Clear
                        </a>
                        <button class="btn btn-primary mx-3" type="submit">
                            <i class="feather icon-search"></i>&nbsp;Search
                        </button>
                    """),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )
