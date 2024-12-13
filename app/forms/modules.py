from typing import *
from django.utils.text import capfirst
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field, HTML
from app.models.modules import *
from ridt import settings


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
    type_of_filing = forms.ChoiceField(widget=forms.Select(), choices=[("Patent", "Patent")], required=False)

    class Meta:
        model = Family
        fields = "__all__"
        exclude = ["case_no"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column("internal_title", "formal_title", "status", "sub_filing",
                               "type_of_filing",  css_class="col-md-4 small-input"),
                        Column("primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal","licenced",
                               
                               css_class="col-md-4 small-input"),
                        Column("applicant", "cost_centre", "cost_centre_code", "keywords" ,"licensor",
                               css_class="col-md-4 small-input"),
                    ),
                    css_class="col-12"
                )
            )
        )

        # Apply custom styles to each field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 8px; height: auto; padding: 2px 3px; margin-bottom: 2px;'

        # Apply custom styles to labels
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({'style': 'font-size: 10px; margin-bottom: 2px;'})

        # Additional styling for form groups and buttons
        self.helper.attrs = {
            'class': 'small-form',
            'style': 'margin-bottom: 3px;'
        }


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
                        Column("case_no", "internal_title", "formal_title", "status", "sub_filing",
                               "type_of_filing", "licenced", "licensor", css_class="col-md-4"),
                        Column("primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                               "applicant", "cost_centre", "cost_centre_code", "keywords",
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
                            "formal_title", "status","filing_type", "sub_filing_type", "sub_status", "internal_title", 'design_file',
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

        # Set date fields with a date picker
        date_fields = ["applicaation_date", "registration_date", "next_tax_date", "expiry_date"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.TextInput(attrs={'type': 'date'})

        # Custom widget for picture_of_trademark (hidden in form)
        self.fields['picture_of_trademark'].widget = forms.ClearableFileInput(attrs={
            'class': 'custom-file-input d-none',  # Hide the field in the form
        })

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column(
                            "family", "country", "trademark_name", "type_of_trademark", "trademark_priority_no",
                            "trademark_application_no", "trademark_registration_no",
                            css_class="col-md-12"
                        ),
                    ),
                    css_class="col-md-6"
                ),
                Column(
                    Row(
                        Column(
                            "primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                            "applicaation_date", "registration_date",
                            css_class="col-md-6 col-sm-12"
                        ),
                        Column(
                            "associate", "associate_ref", "next_tax_date", "taxes_paid_by", 
                            "expiry_date","classes","type_of_filing",
                            css_class="col-md-6 col-sm-12"
                        ),
                    ),
                    css_class="col-md-6"
                ),
                # Hidden image field in form
                Column(
                    Field(
                        "picture_of_trademark",
                        css_class="col-md-12 d-none"
                    ),
                    css_class="col-md-12"
                )
            )
        )

    def display_image(self):
        """ Display image if it exists. """
        if self.instance and self.instance.picture_of_trademark:
            return self.instance.picture_of_trademark.url
        return None

    def clean(self):
        """ Debugging validation errors """
        cleaned_data = super().clean()

        # Example of debugging for missing required fields
        for field, value in cleaned_data.items():
            if not value and self.fields[field].required:
                print(f"Missing required field: {field}")

        # Add other validation checks if needed

        return cleaned_data


class PatentForm(forms.ModelForm):
    PCT_Country = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(), 
        widget=forms.SelectMultiple, 
        required=False, 
        label="PCT Country"
    )
    inventor = forms.ModelMultipleChoiceField(
        queryset=Inventor.objects.all(), 
        widget=forms.SelectMultiple, 
        required=False, 
        label="Inventor"
    )
    sub_filing_type = forms.ChoiceField(
        choices=[
            ('', "---"), 
            ('PCT National Phase', 'PCT National Phase'), 
            ('Divisional', 'Divisional'), 
            ('Non Provisional', 'Non Provisional'),
            ('US Continuation', 'US Continuation'), 
            ('EP National', 'EP National'),
            ('EP Regional', 'EP Regional'), 
            ('EP-PCT National', 'EP-PCT National'),
            ("US Continuation in Part", "US Continuation in Part")
        ],
        required=False, 
        label="Sub Filing Type"
    )

    class Meta:
        model = Patent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PCT_Country'].queryset = Country.objects.all()

        date_fields = [
            'priority_provisional_date', 'PCT_application_Date',
            'application_date', 'publication_date', 'grant_date',
            'next_annuity_due'
        ]
        for field_name in date_fields:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.DateInput(
                    format='%d-%m-%Y',
                    attrs={
                        'type': 'text',
                        'placeholder': 'dd-mm-yyyy',
                        'class': 'form-control form-control-sm datepicker',
                        'style': 'font-size: 13px; height: 38px; padding: 5px 10px; margin-bottom: 1px;'
                    }
                )
                self.fields[field_name].input_formats = ['%d-%m-%Y']
        # Initialize Crispy Form Helper
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'

        # Layout structure for three columns
        self.helper.layout = Layout(
            Row(
                # Column 1
                Column(
                    Field('case_no'),
                    
                    Field('internal_title'),
                    Field('formal_title'),
                    Field('case_type'),
                    Field('status'),
                    Field('sub_status'),
                    Field('filing_type'),
                    Field('sub_filing_type'),
                    Field('cost_centre'),
                    Field('priority_provisional_application_no'),
                    Field('PCT_application_no'),
                    Field('application_no'),
                    Field('publication_no'),
                    Field('grant_number'),
                    css_class="col-md-4"
                ),
                
                # Column 2 (with dates aligned horizontally next to their respective fields)
                Column(
                    Field('country'),
                    Field('primary_attorney'),
                    Field('secondary_attorney'),
                    Field('primary_paralegal'),
                    Field('secondary_paralegal'),
                    Field('inventor'),
                    HTML('<div class="form-group" style="height: 20px;"></div>'), 
                    HTML('<div class="form-group" style="height: 20px;"></div>'), 
                    HTML('<div class="form-group" style="height: 20px;"></div>'), 
                    Field("official_number"),
                    Field('cost_centre_code'),
                    Field('priority_provisional_date'),
                    HTML('<div class="form-group" style="height: 10px;"></div>'), 
                    Field('PCT_application_Date'),
                    Field('application_date'),
                    HTML('<div class="form-group" style="height: 5px;"></div>'), 
                    Field('publication_date'),
                    Field('grant_date'),
                    css_class="col-md-4"
                ),
                
                # Column 3
                Column(
                    Field('associate'),
                    Field('associate_ref'),
                    Field('associate_2'),
                    Field('associate_2_ref'),
                    Field('licence'),
                    Field('next_annuity_due'),
                    Field('annuity_no'),
                    Field('taxs_paid_by'),
                    Field('patent_term_no_of_days'),
                    Field('large_small_entity'),
                    css_class="col-md-4"
                ),
            )
        )

        # Apply custom styles to each field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = (
                'font-size: 13px; height: 38px; padding: 5px 10px; margin-bottom: 1px;'
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
                            "family", "formal_title", "case_type", "inventor", "status", "sub_filing_type","filing_type",
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
                            "associate", "associate_ref", "associate_2", "associate_2_ref", "country", "PCT_Country",
                            "licence",
                            "next_annuity_due", "annuity_no", "taxs_paid_by", "patent_term_no_of_days",
                            "large_small_entity",
                            css_class="col-md-6 col-sm-12"  # Modify col-md-6 to col-md-6 col-sm-12
                        ),
                    ),
                    css_class="col-md-6"
                ),
            )
        )
