from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field

from app.models.billing import *

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "customer_name", "item_name", "item_description", "contact_person", "type_of_work",
                    css_class="col-md-6"
                ),
                Column(
                    "telephone_number", "email_address", "fax_number", "payment_status",
                    css_class="col-md-6"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )