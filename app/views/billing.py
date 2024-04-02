from django.shortcuts import render

from app.models import (
    Invoice
)
from app.forms import (
    InvoiceForm
)

def invoices_view(request):
    context = {
        "items": Invoice.objects.all(),
        "form": InvoiceForm
    }
    return render(request, "app/billing/invoices.html", context)