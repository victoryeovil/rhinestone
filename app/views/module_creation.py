from django.http.request import HttpRequest
from django.shortcuts import render, HttpResponseRedirect

from app.models.inventions import InventionDisclosure
from app.models.modules import Design, Family, Patent, Trademark

tabs = [
    {"title": "Invention Disclosure(s)", "tab": "inventions/disclosures/", "label": "Invention Disclosure"},
    
    {"title": "Patent Family(ies)", "tab": "modules/families-patent/add/", "label": "Family"},
    {"title": "Design Family(ies)", "tab": "modules/families-design/add/", "label": "Family"},
    {"title": "Trademark Family(ies)", "tab": "modules/families-trademark/add/", "label": "Family"},
    {"title": "Patent Country", "tab": "modules/patents/add/", "label": "Patent"},
    {"title": "Design Country", "tab": "modules/designs/add/", "label": "Design"},
    {"title": "Trademark Country", "tab": "modules/trademarks/add/", "label": "Trademark"},
]

def module_create(request: HttpRequest):
    try:
        # Retrieve all entries from each specified model
        inventions = InventionDisclosure.objects.all()
        patents = Patent.objects.all()
        families = Family.objects.all()
        designs = Design.objects.all()
        trademarks = Trademark.objects.all()

        # Combine all entries into a single list
        items = list(inventions) + list(patents) + list(families) + list(designs) + list(trademarks)
    except Exception as e:
        # Handle any potential exceptions that may arise
        items = []
    
    context = {
        "tabs": tabs,
        "items": items,
    }
    return render(request, "app/address-book/module_c/list.html", context)