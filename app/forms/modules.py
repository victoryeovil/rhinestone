from typing import *
from django.utils.text import capfirst
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field, HTML
from app.models.modules import *


#from bootstrap_datepicker_plus import DatePickerInput

class DeleteForm(forms.Form):
    confirmation = forms.BooleanField(required=True, help_text="Tick box to confirm :)")

    def __init__(self, *args, **kwargs):
        module_name = kwargs.pop("module_name")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "confirmation",
                    css_class="col-12"
                ),
                Column(
                    HTML(f'<a href="/app/modules/{module_name}/list/" class="btn btn-primary">Cancel</a>'),
                    Submit("submit", "Delete", css_class="btn btn-danger mx-3"),
                    css_class="col-12 pt-3 text-center"
                )

            )
        )


class FamilyDesignForm(forms.ModelForm):
    type_of_filing = forms.ChoiceField(widget=forms.Select(), choices=[("Design", "Design")], required=False)

    class Meta:
        model = Family
        fields = "__all__"

    # def __init__(self, data: Optional[Mapping[str, Any]] = ..., files: Optional[Mapping[str, File]] = ..., auto_id: Union[bool, str] = ..., prefix: Optional[str] = ..., initial: Optional[Dict[str, Any]] = ..., error_class: Type[ErrorList] = ..., label_suffix: Optional[str] = ..., empty_permitted: bool = ..., instance: Optional[models.Model] = ..., use_required_attribute: Optional[bool] = ..., renderer: Any = ...) -> None:
    #     super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance, use_required_attribute, renderer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "case_no", css_class="col-md-2"
                ),
                Column(
                    "status", css_class="col-md-2"
                ),
                Column(
                    "internal_title", css_class="col-md-2"
                ),
                Column(
                    "formal_title", css_class="col-md-2"
                ),
                Column(
                    "country", css_class="col-md-2"
                ),
            ),
            Row(
                Column(
                    "sub_status", css_class="col-md-2"
                ),
                Column(
                    "sub_filing", css_class="col-md-2"
                ),
                Column(
                    "type_of_filing", css_class="col-md-2"
                ),
                Column(
                    "licenced", css_class="col-md-2"
                ),
                Column(
                    "secondary_paralegal", css_class="col-md-2"
                ),
                Column(
                    "licensor", css_class="col-md-2"
                ),
            ),
            Row(
                Column(
                    "primary_attorney", css_class="col-md-2"
                ),
                Column(
                    "secondary_attorney", css_class="col-md-2"
                ),
                Column(
                    "primary_paralegal", css_class="col-md-2"
                ),
                Column(
                    "cost_centre", css_class="col-md-2"
                ),
                Column(
                    "cost_centre_code", css_class="col-md-2"
                ),
                Column(
                    "keywords", css_class="col-md-2"
                ),
            ),
        )


class FamilyTrademarkForm(forms.ModelForm):
    # type_of_filing=forms.ChoiceField(widget = forms.Select(), choices=[(i, i) for i in ["Trademark", "Design", "Patent"]],required = False)
    type_of_filing = forms.ChoiceField(widget=forms.Select(), choices=[("Trademark", "Trademark")], required=False)

    class Meta:
        model = Family
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "case_no", css_class="col-md-2"
                ),
                Column(
                    "status", css_class="col-md-2"
                ),
                Column(
                    "internal_title", css_class="col-md-2"
                ),
                Column(
                    "formal_title", css_class="col-md-2"
                ),
                Column(
                    "country", css_class="col-md-2"
                ),
            ),
            Row(
                Column(
                    "sub_status", css_class="col-md-2"
                ),
                Column(
                    "sub_filing", css_class="col-md-2"
                ),
                Column(
                    "type_of_filing", css_class="col-md-2"
                ),
                Column(
                    "licenced", css_class="col-md-2"
                ),
                Column(
                    "secondary_paralegal", css_class="col-md-2"
                ),
                Column(
                    "licensor", css_class="col-md-2"
                ),
            ),
            Row(
                Column(
                    "primary_attorney", css_class="col-md-2"
                ),
                Column(
                    "secondary_attorney", css_class="col-md-2"
                ),
                Column(
                    "primary_paralegal", css_class="col-md-2"
                ),
                Column(
                    "cost_centre", css_class="col-md-2"
                ),
                Column(
                    "cost_centre_code", css_class="col-md-2"
                ),
                Column(
                    "keywords", css_class="col-md-2"
                ),
            ),
        )


class FamilyPatentForm(forms.ModelForm):
    # type_of_filing=forms.ChoiceField(widget = forms.Select(), choices=[(i, i) for i in ["Trademark", "Design", "Patent"]],required = False)
    type_of_filing = forms.ChoiceField(widget=forms.Select(), choices=[("Patent", "Patent")], required=False)

    class Meta:
        model = Family
        fields = "__all__"
        exclude = ["case_no"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column("internal_title", "formal_title", "status", "sub_status", "sub_filing",
                               "type_of_filing", "licenced", "licensor", css_class="col-md-4"),
                        Column("primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                               "applicant", "inventor", "cost_centre", "cost_centre_code", "keywords",
                               css_class="col-md-4"),
                        #Column( css_class="col-md-4"),
                        #Column( css_class="col-md-4"),

                    ),
                    css_class="col-12"
                ),
                Column(

                    css_class="col-md-4"
                ),
                Column(
                    Row(
                        Column(

                            css_class="col-md-4"
                        ),
                        Column(
                            Row(
                                Column(
                                    css_class="col-md-6"
                                ),
                            ),
                            css_class="col-12"
                        ),
                        Column(

                            css_class="col-md-6"
                        ),
                    ),
                    css_class="col-md-8"
                ),
                # Column(
                #     Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                #     Submit("submit", "Save", css_class="btn btn-primary"),
                #     css_class="col-12 pt-3 text-center"
                # )

            )
        )
        # Column(
        #     Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
        #     Submit("submit", "Save", css_class="btn btn-primary"),
        #     css_class="col-12 pt-3 text-center"
        # )


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column("case_no", "internal_title", "formal_title", "status", "sub_status", "sub_filing",
                               "type_of_filing", "licenced", "licensor", css_class="col-md-4"),
                        Column("primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                               "applicant", "inventor", "cost_centre", "cost_centre_code", "keywords",
                               css_class="col-md-4"),
                        #Column( css_class="col-md-4"),
                        #Column( css_class="col-md-4"),

                    ),
                    css_class="col-12"
                ),
                Column(

                    css_class="col-md-4"
                ),
                Column(
                    Row(
                        Column(

                            css_class="col-md-4"
                        ),
                        Column(
                            Row(
                                Column(
                                    css_class="col-md-6"
                                ),
                            ),
                            css_class="col-12"
                        ),
                        Column(

                            css_class="col-md-6"
                        ),
                    ),
                    css_class="col-md-8"
                ),
                # Column(
                #     Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                #     Submit("submit", "Save", css_class="btn btn-primary"),
                #     css_class="col-12 pt-3 text-center"
                # )

            )
        )


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column("family", css_class="col-md-12"),
                    ),
                    Row(
                        Column(
                            "formal_title", "status", "sub_filing_type", "sub_status", "internal_title", 'design_file',
                            "country", "design_priority_no", "design_application_no",
                            css_class="col-md-12"
                        ),
                    ),
                    css_class="col-md-4"
                ),
                Column(
                    Row(
                        Column(
                            "primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                            css_class="col-md-6"
                        ),
                        Column(
                            "associate", "associate_ref", "associate_2", "associate_2_ref", "registration_no",
                            css_class="col-md-6"
                        ),
                        Column(
                            Row(
                                Column("cost_centre", css_class="col-md-6"),
                                Column("cost_centre_code", css_class="col-md-6"),
                            ),
                            css_class="col-12"
                        ),
                        Column(
                            "licence", "licensor", "no_of_drawings", "no_of_views",
                            css_class="col-md-6 col-12"
                        ),
                        Column(
                            "next_taxes_date", "next_annuity_no", "taxes_paid_by", "expired_date",
                            css_class="col-md-6"
                        ),
                    ),
                    css_class="col-md-6"
                ),
            )
        )

    def capitalize_labels(self):
        for field_name, field in self.fields.items():
            field.label = capfirst(field.label)


class TrademarkForm(forms.ModelForm):
    class Meta:
        model = Trademark
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column("family", "country", "picture_of_trademark", "trademark_priority_no",
                               "trademark_application_no", "trademark_registration_no",
                               css_class="col-md-12"
                               ),
                    ),
                    css_class="col-md-4"
                ),
                Column(
                    Row(
                        Column(
                            "primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                            "date", "date",
                            css_class="col-md-6"
                        ),
                        Column(
                            "associate", "associate_ref", "next_tax_date", "taxes_paid_by", "does_it_expire", "date",
                            css_class="col-md-6"
                        ),
                    ),
                    css_class="col-md-6"
                ),

            ),

            # Column(
            #     Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
            #     Submit("submit", "Save", css_class="btn btn-primary"),
            #     css_class="col-12 pt-3 text-center"
            # )

        )


class PatentForm(forms.ModelForm):
    # status=forms.ChoiceField(widget = forms.Select(),
    # # choices=[(i, i) for i in ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired", "Published"]],required = False,)
    PCT_Country = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), widget=forms.SelectMultiple,
                                                 required=False, label="PCT Country")
    inventor = forms.ModelMultipleChoiceField(queryset=Inventor.objects.all(), widget=forms.SelectMultiple,
                                              required=False, label="Inventor")

    class Meta:
        model = Patent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PCT_Country'].queryset = Country.objects.all()

        # Set the choices for PCT_Country field
        #self.fields['PCT_Country'].choices = [(country["code"], country["name"]) for country in data.countries.PCT_COUNTRIES]
        date_fields = ["priority_provisional_date", "PCT_application_Date", "application_date", "publication_date",
                       "grant_date", "next_annuity_due"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date'})

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            "case_no", "internal_title", "formal_title", "case_type", "status", "sub_status",
                            "sub_filing_type", "cost_centre", "cost_centre_code", "priority_provisional_application_no",
                            "PCT_application_no", "application_no", "publication_no", "grant_number",
                            css_class="col-md-12"
                        ),
                    ),
                    css_class="col-md-6"
                ),
                Column(
                    Row(
                        Column(
                            "country", "primary_attorney", "secondary_attorney", "primary_paralegal",
                            "secondary_paralegal", "inventor", "priority_provisional_date", "PCT_application_Date",
                            "application_date", "publication_date", "grant_date",
                            css_class="col-md-6 col-sm-12"  # Modify col-md-6 to col-md-6 col-sm-12
                        ),
                        Column(
                            "associate", "associate_ref", "associate_2", "associate_2_ref", "PCT_Country", "licence",
                            "next_annuity_due", "annuity_no", "taxs_paid_by", "patent_term_no_of_days",
                            "large_small_entity",
                            css_class="col-md-6 col-sm-12"  # Modify col-md-6 to col-md-6 col-sm-12
                        ),
                    ),
                    css_class="col-md-6"
                ),
            )
        )


class PatentPCTForm(forms.Form):
    pct_country = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), widget=forms.CheckboxSelectMultiple,
                                                 required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'pct_country', )


class PatentForms(forms.ModelForm):
    # status=forms.ChoiceField(widget = forms.Select(),
    # # choices=[(i, i) for i in ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired", "Published"]],required = False,)
    PCT_Country = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), widget=forms.SelectMultiple,
                                                 required=False, label="PCT Country")
    inventor = forms.ModelMultipleChoiceField(queryset=Inventor.objects.all(), widget=forms.SelectMultiple,
                                              required=False, label="Inventor")

    class Meta:
        model = Patent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PCT_Country'].queryset = Country.objects.all()

        # Set the choices for PCT_Country field
        #self.fields['PCT_Country'].choices = [(country["code"], country["name"]) for country in data.countries.PCT_COUNTRIES]
        date_fields = ["priority_provisional_date", "PCT_application_Date", "application_date", "publication_date",
                       "grant_date", "next_annuity_due"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date'})

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            "family", "formal_title", "case_type", "inventor", "status", "sub_filing_type",
                            "sub_status", "cost_centre", "priority_provisional_application_no", "PCT_application_no",
                            "application_no", "publication_no", "grant_number", "cost_centre_code",
                            css_class="col-md-12"
                        ),
                    ),
                    css_class="col-md-6"
                ),
                Column(
                    Row(
                        Column(
                            "internal_title", "primary_attorney", "secondary_attorney", "primary_paralegal",
                            "secondary_paralegal", "priority_provisional_date", "PCT_application_Date",
                            "application_date", "publication_date", "grant_date",
                            css_class="col-md-6 col-sm-12"  # Modify col-md-6 to col-md-6 col-sm-12
                        ),
                        Column(
                            "associate", "associate_ref", "associate_2", "associate_2_ref", "country", "PCT_Country", "licence",
                            "next_annuity_due", "annuity_no", "taxs_paid_by", "patent_term_no_of_days",
                            "large_small_entity",
                            css_class="col-md-6 col-sm-12"  # Modify col-md-6 to col-md-6 col-sm-12
                        ),
                    ),
                    css_class="col-md-6"
                ),
            )
        )
