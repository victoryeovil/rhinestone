from django.shortcuts import render

from app.models import (
    InventionDisclosure
)
from app.forms import (
    InventionDisclosureForm
)
from app.forms.files import (
    FileForm
)
def invention_disclosures_view(request):  
    context = {
        "items": InventionDisclosure.objects.all(),
        "form": InventionDisclosureForm,
        "file_form" : FileForm
    }
    return render(request, "app/inventions/temp.html", context)