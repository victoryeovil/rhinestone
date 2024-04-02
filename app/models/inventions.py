from django.db import models

from .fields import FileField
from .base import BaseModel


class InventionDisclosure(BaseModel):
    id_ref_number = models.CharField(max_length=10)
    title = models.CharField(max_length=128)
    status = models.CharField(max_length=64, choices=[(i, i) for i in ["OPENED", "PENDING", "UNDER REVIEW", "PROCESSED", "NOT PROCESSED", "ABANDONED", "SOLD"]])
    is_there_an_agreement = models.CharField(max_length=3, choices=[(i, i) for i in ["Yes", "No"]])
    date_file_opened = models.DateField(blank=True, null=True)
    date_of_invention = models.DateField(blank=True, null=True)
    keyword = models.CharField(max_length=256, blank=True, null=True)
    cost_centre = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in ["Cost-1", "Cost-2"]])
    cost_centre_code = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in ["Applicant-1", "Applicant-2"]])
    joint_venture = models.CharField(max_length=3, choices=[(i, i) for i in ["Yes", "No"]])
    primary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL, blank=True, null=True, related_name="primary_attorney_set")
    secondary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL, blank=True, null=True, related_name="secondary_attorney_set")
    primary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL, blank=True, null=True, related_name="primary_paralegal_set")
    secondary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL, blank=True, null=True, related_name="secondary_paralegal_set")
    invention_description = models.TextField(max_length=512, blank=True, null=True)
    general_notes = models.TextField(max_length=512, blank=True, null=True)
    proposed_inventors = models.CharField(max_length=512, blank=True, null=True)
    confirmed_inventors = models.TextField(max_length=512, blank=True, null=True)
    reasons_of_approval_or_rejection = models.TextField(max_length=512, blank=True, null=True)
    approved_for_filing = models.CharField(max_length=3, choices=[(i, i) for i in ["Yes", "No"]])
    approval_or_rejection_date = models.DateField(blank=True, null=True)
    approved_by = models.CharField(max_length=256, blank=True, null=True)
    files = models.ManyToManyField("app.File")
