from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field

from app.models.contacts import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "phone", "email", "address_line_1", css_class="col-lg-6 small-input"),
                Column("address_line_2", "address_city", "address_state", "type", css_class="col-lg-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 8px; height: auto; padding: 2px 5px; margin-bottom: 2px;'


class InventorForm(forms.ModelForm):
    is_applicant = forms.BooleanField(required=False, label="Is Applicant")

    class Meta:
        model = Inventor
        exclude = ['type', 'contract', 'date_of_contact']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        date_fields = ["commencement_date", "date_of_employment_termination"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date'})
        self.helper.layout = Layout(
            Row(
                Column("title", "name", "surname", "nationality", "county_state", "profession", "employer_name", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_line_3", "zip_postal_code", "commencement_date", "email_of_future_contact", "notes", "is_applicant", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class ApplicantForm(forms.ModelForm):
    is_inventor = forms.BooleanField(required=False, label="Is Inventor")
    name = forms.CharField(required=True, label="Applicant Name")

    class Meta:
        model = Applicant
        exclude = ['type']
        widgets = {
            'date_of_incorporation': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        date_fields = ["date_of_incorporation"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date'})
        self.helper.layout = Layout(
            Row(
                Column("name", "phone", "email", "nationality", "country_of_registration", "date_of_incorporation", "is_inventor","customer_instructions", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_city", "address_state", "zip_postal_code", "notes", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


# class ApplicantForm(forms.ModelForm):
#     is_inventor = forms.BooleanField(required=False, label="Is Inventor")
#
#     class Meta:
#         model = Applicant
#         exclude = ['type']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_class = 'form-horizontal'
#         self.helper.layout = Layout(
#             Row(
#                 Column(
#                     "name", "surname", "phone", "email", "nationality", "country_of_registration",
#                     "is_inventor",
#                     css_class="col-md-6"
#                 ),
#                 Column(
#                     "address_line_1", "address_line_2", "address_city",
#                     "address_state", "zip_postal_code",
#                     "status", "notes",
#                     css_class="col-md-6"
#                 ),
#                 Column(
#                     Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
#                     Submit("submit", "Save", css_class="btn btn-primary"),
#                     css_class="col-12 pt-3 text-center"
#                 )
#             )
#         )


class LicensorForm(forms.ModelForm):
    class Meta:
        model = Licensor
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "surname", "nationality", "date_of_employment_termination", "contractor", "contractor_type", "email_of_future_contact", "employer_name", "notes", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_city", "address_state", "employer_address_line_1", "employer_address_line_2", "employer_address_city", "employer_address_state", "zip_postal_code", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class LicenseeForm(forms.ModelForm):
    class Meta:
        model = Licensee
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        date_fields = ["date_of_incorporation"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date'})
        self.helper.layout = Layout(
            Row(
                Column("name", "surname", "email", "phone", "nationality", "country_of_registration", "date_of_incorporation", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_city", "address_state", "zip_postal_code", "notes", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class ConsultantForm(forms.ModelForm):
    class Meta:
        model = Consultant
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "surname", "email", "phone", "nationality", "country_of_registration", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_city", "address_state", "zip_postal_code", "notes", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'



class AssociateForm(forms.ModelForm):
    class Meta:
        model = Associate
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.fields['name'].label = "Associate Name"
        self.fields['email'].label = "Email address(es)"
        self.fields['address_state'].label = "Country/State"
        self.fields['zip_postal_code'].label = "Zip/Postal Code"
        self.fields['contact_person'].label = "Contact Person(s)"
        self.helper.layout = Layout(
            Row(
                Column("name", "phone", "email", "contact_person", "country", "notes", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_city", "address_state", "zip_postal_code", "website", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class ParalegalForm(forms.ModelForm):
    class Meta:
        model = Paralegal
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "surname", "email", "notes", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'



class AttorneyForm(forms.ModelForm):
    class Meta:
        model = Attorney
        exclude = ['type']  # Exclude the 'type' field from the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "surname", "email", "notes", css_class="col-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class OtherProviderForm(forms.ModelForm):
    class Meta:
        model = OtherProvider
        exclude = ['type', 'MID']
        widgets = {
            'date_of_incorporation': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Other Provider Name"
        self.fields['email'].label = "Email Address"
        self.fields['address_state'].label = "County/State"
        self.fields['zip_code'].label = "Postal/Zip Code"
        self.fields['contact_person'].label = "Contact Person(s)"
        self.fields['country'].widget = forms.Select(choices=data.countries.COUNTRIES_OPTIONS)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("authorizer", "applicants", "contact_person", "phone", "email", "notes", css_class="col-md-6 small-input"),
                Column("address_line_1", "address_line_2", "address_line_3", "address_state", "country", "zip_code","customer_instructions", css_class="col-md-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 11px; height: auto; padding: 2px 3px; margin-bottom: 2px;'


class CostCenterForm(forms.ModelForm):
    class Meta:
        model = CostCenter
        exclude = ['type']  # Exclude the 'type' field from the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.label_class = 'small-label'
        self.helper.field_class = 'small-input'
        self.helper.layout = Layout(
            Row(
                Column("name", "code", css_class="col-6 small-input"),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 14px; height: auto; padding: 2px 5px; margin-bottom: 2px;'