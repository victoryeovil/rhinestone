from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Reset

from app.models import CostCenter
from app.models.inventions import InventionDisclosure
from django.core.exceptions import ValidationError

class InventionDisclosureForm(forms.ModelForm):
    files = forms.FileField( required=False)


    class Meta:
        model = InventionDisclosure
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal small-form'
        # Customizing the choices to display cost_center_no and code separately
        self.fields['cost_centre'].queryset = CostCenter.objects.all()
        self.fields['cost_centre'].label_from_instance = lambda \
            obj: obj.get_cost_center_no_display()  # Display the cost center number

        self.fields['cost_centre_code'].queryset = CostCenter.objects.all()
        self.fields['cost_centre_code'].label_from_instance = lambda obj: obj.get_code_display()  # Display the code
        # Use FileInput widget to allow multiple file uploads
        # self.fields['files'].widget = forms.FileInput(attrs={'multiple': True})

        date_fields = ["date_of_invention", "approval_or_rejection_date", "date_file_opened"]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.TextInput(attrs={'type': 'date'})

        # Layout adjusted to have one row and three columns containing all model fields
        self.helper.layout = Layout(
            Row(
                Column(
                    "id_ref_number",  # Auto-generated ID, can be read-only or hidden in the form
                    "date_file_opened",
                    "title",
                    "status",
                    "keyword",
                    "date_of_invention",
                    "agreement",
                    "approval_or_rejection_date",

                    "joint_venture",

                    css_class="col-lg-4 small-input"
                ),
                Column(
                    "attorney_1",
                    "primary_paralegal",
                    "cost_centre",
                    "approved_for_filing",

                    "approved_by",
                    "proposed_inventors",

                    css_class="col-lg-4 small-input"
                ),
                Column(
                    "attorney_2",
                    "secondary_paralegal",
                    "cost_centre_code",

                    "confirmed_inventors",
                    "reasons_of_approval_or_rejection",

                      # Assuming it's a file upload field
                    css_class="col-lg-4 small-input"
                ),
            ),
            Row(
                Column(
                     "invention_description", "general_notes",
                    css_class="col-12"  # This makes the field span across the entire width
                )
            ),
            Row(
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )

        # Apply custom classes to each field for consistent styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
            field.widget.attrs['style'] = 'font-size: 12;'

    def clean_files(self):
        files = self.cleaned_data.get('files')
        allowed_file_types = ['pdf', 'docx']
        max_size = 10 * 1024 * 1024  # 10MB

        for file in files:
            ext = file.name.split('.')[-1].lower()
            if ext not in allowed_file_types:
                raise ValidationError(f"File type {ext} is not supported.")
            if file.size > max_size:
                raise ValidationError(f"File size exceeds 10MB.")
        return files

    def clean(self):
        cleaned_data = super().clean()
        approved_for_filing = cleaned_data.get('approved_for_filing')
        approval_or_rejection_date = cleaned_data.get('approval_or_rejection_date')

        if approved_for_filing and not approval_or_rejection_date:
            self.add_error('approval_or_rejection_date', 'Approval or rejection date is required if a decision is made.')
        return cleaned_data
