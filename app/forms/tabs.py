from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from app.models.tabs import Action, InventionDocument, InventorCompensation, PriorArtCitedDoc, RelatedCaseLink

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = '__all__'

class PriorArtCitedDocForm(forms.ModelForm):
    class Meta:
        model = PriorArtCitedDoc
        fields = '__all__'

class RelatedCaseLinkForm(forms.ModelForm):
    class Meta:
        model = RelatedCaseLink
        fields = '__all__'

class InventorCompensationForm(forms.ModelForm):
    class Meta:
        model = InventorCompensation
        fields = '__all__'

class InventionDocumentForm(forms.ModelForm):
    class Meta:
        model = InventionDocument
        fields = '__all__'
