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
from app.models.contacts import Applicant, Associate


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
    associate = forms.ModelChoiceField(queryset=Associate.objects.all(), required=False, label="Agent")
    instructor = forms.ModelChoiceField(queryset=Contact.objects.filter(type__in=["Associate", "Client"]), required=False, label="Instructor")
    owner = forms.ModelChoiceField(queryset=Applicant.objects.all(), required=False, label="Owner")
    name = forms.ModelChoiceField(queryset=Contact.objects.all(), required=False, label="Name")
    name_type = forms.ChoiceField(choices=[
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

    # Reference Section
    case_reference = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Case Reference")
    official_number = forms.CharField(required=False, label="Official Number")
    instructor_reference = forms.ModelChoiceField(queryset=Family.objects.values_list('licensor', flat=True).distinct(), required=False, label="Instructor Reference")
    family = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Family")
    Associates = forms.ModelChoiceField(queryset=Contact.objects.filter(type__in=[
        "Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"
    ]), required=False)
    Associate_refs = forms.ModelChoiceField(queryset=Contact.objects.filter(type__in=[
        "Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"
    ]), required=False)
    primary_attorney = forms.ModelChoiceField(queryset=models.Attorney.objects.all(), required=False)
    secondary_attorney = forms.ModelChoiceField(queryset=models.Attorney.objects.all(), required=False)
    type_of_filing = forms.ChoiceField(required=False, choices=[("", "")] + [(i, i) for i in ["Trademark", "Design", "Patent"]])

    # Case Details Section
    case_office = forms.CharField(required=False, label="Case Office")
    case_type = forms.ChoiceField(choices=[(i, i) for i in CASE_TYPE], required=False, label="Case Type")
    country = forms.ChoiceField(choices=data.countries.COUNTRIES_OPTIONS, required=False, label="Country")
    property_type = forms.CharField(required=False, label="Property Type")
    case_category = forms.CharField(required=False, label="Case Category")
    sub_type = forms.CharField(required=False, label="Sub Type")
    basis = forms.CharField(required=False, label="Basis")
    case_class = forms.CharField(required=False, label="Class")

    # Status Section (Checkboxes)
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
            ("Granted(DEA)", "Granted(DEA)"),
            ("Converted", "Converted"),
            ("Expired", "Expired"),
            ("Published", "Published")
        ],
        widget=forms.CheckboxSelectMultiple
    )
    case_status = forms.CharField(required=False, label="Case Status")
    renewal_status = forms.CharField(required=False, label="Renewal Status")

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
                    css_class="card-body"
                ),
                css_class="card mb-3"
            ),
            # Reference Section
            Div(
                Div(
                    Field('case_reference', css_class="form-control"),
                    Field('official_number', css_class="form-control"),
                    Field('instructor_reference', css_class="form-control"),
                    Field('family', css_class="form-control"),
                    Field('Associates', css_class="form-control"),
                    Field('Associate_refs', css_class="form-control"),
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

    def search(self):
        query = Family.objects.all()

        # Apply filters based on the form fields
        if self.cleaned_data['case_reference']:
            query = query.filter(family_no=self.cleaned_data['case_reference'])
        if self.cleaned_data['official_number']:
            query = query.filter(
                models.Q(family_no__icontains=self.cleaned_data['official_number']) |
                models.Q(case_no__icontains=self.cleaned_data['official_number']) |
                models.Q(internal_title__icontains=self.cleaned_data['official_number']) |
                models.Q(formal_title__icontains=self.cleaned_data['official_number'])
            )
        if self.cleaned_data['instructor_reference']:
            query = query.filter(licensor=self.cleaned_data['instructor_reference'])
        if self.cleaned_data['family']:
            query = query.filter(id=self.cleaned_data['family'].id)

        # Add other filters similarly based on the fields
        # ...

        return query