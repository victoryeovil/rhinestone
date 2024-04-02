from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Reset, Button, Field, HTML

from app.models.inventions import *

class InventionDisclosureForm(forms.ModelForm):
    class Meta:
        model = InventionDisclosure
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "id_ref_number", "title", "status", "is_there_an_agreement",
                    css_class="col-lg-4"
                ),
                Column(
                    "date_file_opened", "date_of_invention", "keyword",
                    Row(
                        Column("cost_centre", css_class="col-md-6"),
                        Column("cost_centre_code", css_class="col-md-6"),
                    ), "joint_venture",
                    css_class="col-lg-4"
                ),
                Column(
                    "primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal",
                    css_class="col-lg-4"
                ),
                Column(
                    "invention_description", "general_notes",
                    Row(
                        Column("proposed_inventors", css_class="col-md-6"),
                        Column("confirmed_inventors", css_class="col-md-6"),
                    ),
                    "reasons_of_approval_or_rejection",
                    css_class="col-12"
                ),
                Column(
                    Row(
                        Column("approved_for_filing", css_class="col-lg-4"),
                        Column("approval_or_rejection_date", css_class="col-lg-4"),
                        Column("approved_by", css_class="col-lg-4"),
                    ),
                    css_class="col-12"
                ),
                Column(
                    "files",
                    css_class="col-12"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
                
            )
        )
