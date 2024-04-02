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
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "name", "phone", "email","address_line_1",
                    css_class="col-lg-6"
                ),
                Column(
                    "address_line_2", "address_city", "address_state","type",
                    css_class="col-lg-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )

    


class InventorForm(forms.ModelForm):
    class Meta:
        model = Inventor
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                     "title", 
                    "surname",  "name", "phone", "email",
                      "contract","commencement_date", "date_of_employment_termination", "date_of_contact","employer_name", 
                      "notes",
                    css_class="col-6"
                ),
                Column(
                    "nationality", "type_of_contract", "home", 
                    "country",  
                     "employer_address_line_1", 
                    "employer_address_line_2", "employer_address_city",
                      "employer_address_state", "zip_postal_code", "employer_nationality", 
                      "email_of_future_contact",
                    css_class="col-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )
    


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "name", "surname", "phone",  "email", "nationality","country_of_registration",
                    
                    css_class="col-md-6"
                ),
                Column(
                    "address_line_1", "address_line_2", "address_city", 
                    "address_state", "zip_postal_code",
                    "status","notes",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )



class LicensorForm(forms.ModelForm):
    class Meta:
        model = Licensor
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "name", "surname",
                    "nationality", "date_of_employment_termination", "contractor",
                      "contractor_type", 
                      "email_of_future_contact","employer_name", "notes",
                    css_class="col-md-6"
                ),
                Column(
                    "address_line_1", 
                    "address_line_2", "address_city", "address_state", 
                     "employer_address_line_1",
                      "employer_address_line_2", "employer_address_city", 
                      "employer_address_state","zip_postal_code", 
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )

        

class LicenseeForm(forms.ModelForm):
    class Meta:
        model = Licensee
        exclude = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "name", "surname",  "email",
                    "phone", "nationality","country_of_registration","date_of_incorporation",
                    css_class="col-md-6"
                ),
                Column(
                    "address_line_1",
                    "address_line_2", "address_city", "address_state","zip_postal_code",   "notes",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )



class ConsultantForm(forms.ModelForm):
    class Meta:
        model = Consultant
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "name","surname", 
                        "email", "phone", "nationality","country_of_registration", 
                    css_class="col-md-6"
                ),
                Column(
            "address_line_1","address_line_2", "address_city", "address_state","zip_postal_code", "notes",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )

   
        

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                   "name", "surname", "phone", "email", "fax_number", "office_contact", "email_of_future_contact",  "contact_person",
                    css_class="col-md-6"
                ),
                Column(
                    "address_line_1", "address_line_2", "address_city", "address_state","zip_postal_code","website",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )
   


class ParalegalForm(forms.ModelForm):
    class Meta:
        model = Paralegal
        exclude = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                 "name", "surname","country_of_registration", "email", "phone", "notes",
                    css_class="col-md-6"
                ),
                Column(
                    "address_line_1", "address_line_2", "address_city", "address_state","zip_postal_code",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )

        



class AttorneyForm(forms.ModelForm):
    class Meta:
        model = Attorney
        exclude = ['type']  # Exclude the 'type' field from the form
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                     "name", "surname",  "email", "phone", "nationality","notes",
                    css_class="col-6"
                ),
                Column(
                    "address_line_1", "address_line_2", "address_city","address_state", "country_of_registration", "zip_postal_code",
                    css_class="col-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )



