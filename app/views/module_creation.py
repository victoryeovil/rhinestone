from django.http.request import HttpRequest
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.db.models import Model
from app.forms.inventions import InventionDisclosureForm
from app.forms.modules import DesignForm, FamilyDesignForm, FamilyForm, FamilyPatentForm, FamilyTrademarkForm, PatentForm, TrademarkForm
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

# def module_create(request: HttpRequest):
#     context = {
#         "tabs": tabs,
#         "inventions": InventionDisclosure.objects.all(),
#         "patents": Patent.objects.all(),
#         "families": Family.objects.all(),
#         "designs": Design.objects.all(),
#         "trademarks": Trademark.objects.all(),
#     }
#     return render(request, "app/address-book/module_c/list.html", context)


def module_create(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        # Handle form submissions
        forms = {
            'invention': InventionDisclosureForm(request.POST),
            'patent_family': FamilyPatentForm(request.POST),
            'design_family': FamilyDesignForm(request.POST),
            'trademark_family': FamilyTrademarkForm(request.POST),
            'patent_country': PatentForm(request.POST),
            'design_country': DesignForm(request.POST),
            'trademark_country': TrademarkForm(request.POST),
        }

        form = forms.get(form_type)
        if form and form.is_valid():
            form.save()
            return redirect('module_create')

    # Helper function to get all field names and values
    def get_model_data(queryset):
        data = []
        for instance in queryset:
            if isinstance(instance, Model):
                data.append(model_to_dict(instance))
        return data

    # Dynamic extraction of model fields and values
    context = {
        "inventions": get_model_data(InventionDisclosure.objects.all()),
        "patents": get_model_data(Patent.objects.all()),
        "families": get_model_data(Family.objects.all()),
        "designs": get_model_data(Design.objects.all()),
        "trademarks": get_model_data(Trademark.objects.all()),
        "invention_form": InventionDisclosureForm(),
        "patent_family_form": FamilyPatentForm(),
        "design_family_form": FamilyDesignForm(),
        "trademark_family_form": FamilyTrademarkForm(),
        "patent_country_form": PatentForm(),
        "design_country_form": DesignForm(),
        "trademark_country_form": TrademarkForm(),
    }
    return render(request, "app/address-book/module_c/list.html", context)
