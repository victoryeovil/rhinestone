from typing import *
from django.db.models import Q
from django import forms
from django.core.files.base import File
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field, HTML
from itertools import chain
from app import models
from app import data
from app.functions.chunk import chunk
from app.models import (
    Family, Patent, Trademark, Design, BaseModel,
    User, Contact, InventionDisclosure, Invoice
)


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
    


class HomeSearchForm(forms.Form):
    _official_numbers__icontains = forms.CharField(required=False, label="Official Number")
    official = _official_numbers__icontains
    _titles__icontains = forms.CharField(required=False, label="Title")
    titles = _titles__icontains
    primary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
    secondary_attorney = forms.ModelChoiceField(models.Attorney.objects.all(), required=False)
    type_of_filing = forms.ChoiceField(required=False, choices=[("","")] + [(i, i) for i in ["Trademark", "Design", "Patent"]])
    _Associates = forms.ModelChoiceField(
        models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
        required=False
    )
    _Associate_refs = forms.ModelChoiceField(
        models.Contact.objects.filter(type__in=["Inventor", "Applicant", "Licensor", "Licensee", "Consultant", "Associate", "Paralegal", "Attorney"]),
        required=False
    )
    status__in = forms.MultipleChoiceField(required=False, label="Status", choices=[("","")] + [(i, i) for i in ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired", "Published"]])
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
                #Column("query", css_class="col-12")
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