from django import forms
from app.models.files import File
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column , Reset , Submit
# from .base import BaseForm
# from .fields import ImageField, FileField


# class FileForm(BaseForm):
#     field = FileField(upload_to="files")
#     Form = forms.CharField(max_length=64)
#     instance_id = forms.IntegerField()


# class Image(FileForm):
#     field = ImageField(upload_to="files")


class FileForm(forms.ModelForm):
    field = forms.FileField(
        widget=forms.FileField(widget=forms.ClearableFileInput(), required=False)
    )

    class Meta:
        model = File
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Row(
                Column(
                    "field",
                    css_class="col-lg-4"
                ),
                Column(
                    "model",
                    css_class="col-lg-4"
                ),
                Column(
                    "instance_id",
                    css_class="col-lg-4"
                ),
                Column(
                    Reset("Reset", "Reset", css_class="btn btn-outline-secondary"),
                    Submit("submit", "Save", css_class="btn btn-primary"),
                    css_class="col-12 pt-3 text-center"
                )
            )
        )
