from django import forms
from django.forms.widgets import SelectMultiple

class MultiSelectDropdownWidget(SelectMultiple):
    template_name = 'app/multiselect_dropdown_widget.html'