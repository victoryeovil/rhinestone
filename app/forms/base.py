from django import forms


class BaseForm(forms.Form):
    
    class Meta:
        abstract = True
