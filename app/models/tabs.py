from django.db import models

from app.models.contacts import Applicant
from app.models.inventions import InventionDisclosure


class Action(models.Model):
    invention = models.ForeignKey(InventionDisclosure, on_delete=models.CASCADE, related_name='actions')
    action_code = models.CharField(max_length=20, blank=True, null=True)
    spell_out = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    taken_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    responsible_person = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class PriorArtCitedDoc(models.Model):
    invention = models.ForeignKey(InventionDisclosure, on_delete=models.CASCADE, related_name='prior_art_docs')
    patentee_applicant = models.ForeignKey(Applicant,max_length=100, blank=True, null=True)
    application_no = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    application_date = models.DateField(blank=True, null=True)

class RelatedCaseLink(models.Model):
    invention = models.ForeignKey(InventionDisclosure, on_delete=models.CASCADE, related_name='related_cases')
    reference_number = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    application_number = models.CharField(max_length=50)
    application_date = models.DateField(blank=True, null=True)

class InventorCompensation(models.Model):
    invention = models.ForeignKey(InventionDisclosure, on_delete=models.CASCADE, related_name='compensations')
    inventor_name = models.CharField(max_length=100)
    percentage_contributed = models.DecimalField(max_digits=5, decimal_places=2)
    compensation_calculation = models.DecimalField(max_digits=10, decimal_places=2)
    compensation_paid = models.BooleanField(default=False)
    date_compensation_paid = models.DateField(blank=True, null=True)

class InventionDocument(models.Model):
    invention = models.ForeignKey(InventionDisclosure, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    document_name = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=100)
    date_uploaded = models.DateField(auto_now_add=True)
