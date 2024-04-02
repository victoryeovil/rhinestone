from django.db import models

from .base import BaseModel

class Invoice(BaseModel):
    customer_name = models.CharField(max_length=128)
    item_name = models.CharField(max_length=128, blank=True, null=True)
    item_description = models.CharField(max_length=128, blank=True, null=True)
    contact_person = models.CharField(max_length=128, blank=True, null=True)
    type_of_work = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in ['customer_name', 'item_name', 'item_description', 'contact_person', 'type_of_work', 'telephone_number', 'email_address', 'fax_number', 'payment_status']])
    telephone_number = models.CharField(max_length=16, blank=True, null=True)
    email_address = models.EmailField(max_length=128, blank=True, null=True)
    fax_number = models.CharField(max_length=128, blank=True, null=True)
    payment_status = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in ["Paid", "Pending", "Not-Paid"]])
