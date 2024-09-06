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
        self.helper.form_class = 'form-horizontal small-form'
        self.helper.layout = Layout(
            Row(
                Column(
                    "id_ref_number", "title", "status", "is_there_an_agreement", "invention_description", "general_notes",
                    "approved_for_filing", "files",
                    css_class="col-lg-4 small-input"
                ),
                Column(
                    "date_file_opened", "date_of_invention", "keyword", "cost_centre", "cost_centre_code", "joint_venture", "proposed_inventors",
                    "approval_or_rejection_date",
                    css_class="col-lg-4 small-input"
                ),
                Column(
                    "primary_attorney", "secondary_attorney", "primary_paralegal", "secondary_paralegal", "confirmed_inventors", 
                    "reasons_of_approval_or_rejection", "approved_by",
                    css_class="col-lg-4 small-input"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        # Apply custom classes to each field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 8px;'
