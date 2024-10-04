from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .base import BaseModel


class InventionDisclosure(BaseModel):
    id_ref_number = models.CharField(
        max_length=10, unique=True, blank=True, verbose_name="Reference ID"
    )
    title = models.CharField(
        max_length=128, verbose_name="Title"
    )
    status = models.CharField(
        max_length=64, choices=[(i, i) for i in ["OPENED", "PENDING", "UNDER REVIEW", "PROCESSED", "NOT PROCESSED", "ABANDONED", "SOLD"]],
        verbose_name="Status"
    )
    agreement = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=False, verbose_name="Agreement"
    )
    date_file_opened = models.DateField(
        blank=True, null=True, verbose_name="Date File Opened"
    )
    date_of_invention = models.DateField(
        blank=True, null=True, verbose_name="Date of Invention"
    )
    keyword = models.CharField(
        max_length=256, blank=True, null=True, verbose_name="Keyword(s)"
    )
    cost_centre = models.ForeignKey(
        "app.CostCenter", on_delete=models.SET_NULL, blank=True, null=True, related_name="invention_cost_centre",
        verbose_name="Cost Centre"
    )
    cost_centre_code = models.ForeignKey(
        "app.CostCenter", on_delete=models.SET_NULL, blank=True, null=True, related_name="invention_cost_centre_code",
        verbose_name="Cost Centre Code"
    )
    joint_venture = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], verbose_name="Joint Venture"
    )

    attorney_1 = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, blank=True, null=True, related_name="attorney_1_set",
        verbose_name="Attorney 1"
    )
    attorney_2 = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, blank=True, null=True, related_name="attorney_2_set",
        verbose_name="Attorney 2"
    )
    primary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, blank=True, null=True, related_name="primary_paralegal_set",
        verbose_name="Paralegal 1"
    )
    secondary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, blank=True, null=True, related_name="secondary_paralegal_set",
        verbose_name="Paralegal 2"
    )

    invention_description = models.TextField(
        max_length=512, blank=True, null=True, verbose_name="Invention Description"
    )
    general_notes = models.TextField(
        max_length=512, blank=True, null=True, verbose_name="General Notes"
    )
    proposed_inventors = models.TextField(
        max_length=512, blank=True, null=True, verbose_name="Proposed Inventors"
    )
    confirmed_inventors = models.TextField(
        max_length=512, blank=True, null=True, verbose_name="Confirmed Inventors"
    )
    reasons_of_approval_or_rejection = models.TextField(
        max_length=512, blank=True, null=True, verbose_name="Reasons of Approval/Rejection"
    )
    approved_for_filing = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], verbose_name="Approved for Filing"
    )
    approval_or_rejection_date = models.DateField(
        blank=True, null=True, verbose_name="Approval/Rejection Date"
    )
    approved_by = models.ForeignKey(
        "app.Contact", blank=True, null=True, verbose_name="Approved By", on_delete=models.SET_NULL
    )

    files = models.ManyToManyField(
        "app.File", verbose_name="Attached Files"
    )
    joint_venture_with_whom = models.CharField(
        max_length=256, blank=True, null=True, verbose_name="Joint Venture With Whom"
    )

# Signal for auto-generating the Reference ID
@receiver(pre_save, sender=InventionDisclosure)
def auto_generate_id_ref_number(sender, instance, **kwargs):
    if not instance.id_ref_number:
        last_instance = sender.objects.all().order_by('id').last()
        if last_instance:
            last_id = int(last_instance.id_ref_number.split('-')[1])
            instance.id_ref_number = f'ID-{last_id + 1:04d}'
        else:
            instance.id_ref_number = 'ID-0001'
