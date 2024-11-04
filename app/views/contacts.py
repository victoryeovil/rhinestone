from django.shortcuts import render, HttpResponseRedirect
from django.http.request import HttpRequest

from django.contrib import messages
from django.utils.datastructures import MultiValueDict
import logging

from app.forms.contacts import CostCenterForm
from app.models import (
    Contact,
    Inventor,
    Applicant,
    Licensor,
    Licensee,
    Consultant,
    Associate,
    Paralegal,
    Attorney, OtherProvider,
)
from app.forms import (
    ContactForm,
    InventorForm,
    ApplicantForm,
    LicensorForm,
    LicenseeForm,
    ConsultantForm,
    AssociateForm,
    ParalegalForm,
    AttorneyForm,
    DeleteForm, OtherProviderForm,

)
from app.models.contacts import CostCenter

tabs = [
    {"title": "Contact(s)", "tab": "contacts", "label": "Contact"},
    {"title": "Inventor(s)", "tab": "inventors", "label": "Inventor"},
    {"title": "Applicant(s)", "tab": "applicants", "label": "Applicant"},
    {"title": "Licensor(s)", "tab": "licensors", "label": "Licensor"},
    {"title": "Licensee(s)", "tab": "licensees", "label": "Licensee"},
    #{"title": "Consultant(s)", "tab": "consultants", "label": "Consultant"},
    {"title": "Associate(s)", "tab": "Associates", "label": "Associate"},
    {"title": "Paralegal(s)", "tab": "paralegals", "label": "Paralegal"},
    {"title": "Attorney(s)", "tab": "attorneys", "label": "Attorney"},
    {"title": "Other Provider(s)", "tab": "other_provider", "label": "Other Provider"},
    {"title": "Cost Center","tab":"costcenter", "label":"Cost Center"}
]


def contacts_view(request: HttpRequest):
    try:
        items = Contact.objects.all()
    except Contact.DoesNotExist:
        items = []

    context = {
        "tabs": tabs,
        "items": [item for item in items if hasattr(item, 'type')],
        "active": "contacts",
        "invalid_items": [item for item in items if not hasattr(item, 'type')],
    }
    return render(request, "app/address-book/contacts/contacts.html", context)


# INVENTORS MODULE

def inventors_view(request):
    tabs[1]['active'] = "show"
    context = {
        "tabs": tabs,
        "active": "inventors",
        "items": Inventor.objects.all(),
        "form": InventorForm
    }
    return render(request, "app/address-book/inventors/inventors.html", context)
logger = logging.getLogger(__name__)

def inventors_detail_view(request: HttpRequest, pk):
    item = Inventor.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "inventors",
    }
    return render(request, "app/address-book/inventors/details.html", context)


# def inventors_create_view(request: HttpRequest):
#     form = InventorForm(initial=MultiValueDict(request.GET).dict())
#     if request.POST:
#         form = InventorForm(data=request.POST)
#         if form.is_valid():
#             attorney = form.save(commit=False)
#             attorney.type = 'Inventor'  # Set the value of 'type' here
#             attorney.save()
#             messages.success(request, "Item successfully created!")
#         else:
#             messages.error(request, f"Failed to create. Form is not valid!")
#     return HttpResponseRedirect("/app/address-book/inventors")

def inventors_create_view(request: HttpRequest):
    form = InventorForm(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = InventorForm(data=request.POST)
        if form.is_valid():
            inventor = form.save(commit=False)
            inventor.type = 'Inventor'  # Set the value of 'type' here
            inventor.save()
            print("saved now saving applicant")
            if form.cleaned_data['is_applicant']:
                Applicant.objects.create(
                    name=inventor.name,
                    surname=inventor.surname,
                    phone=inventor.phone,
                    email=inventor.email,
                    nationality=inventor.nationality,
                    type = 'Applicant',
                    #country=inventor.county_state,
                    # Add other necessary fields from Inventor to Applicant
                    date_of_incorporation=None,  # Provide appropriate value or leave as None
                    status=None,  # Provide appropriate value or leave as None
                    country_of_registration=inventor.county_state,
                    zip_postal_code=inventor.zip_postal_code,
                    notes=inventor.notes,
                    is_inventor=True
                )
            messages.success(request, "Item successfully created!")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/inventors")


def inventors_delete_view(request: HttpRequest, pk):
    item = Inventor.objects.get(id=pk)
    form = DeleteForm(module_name="inventors")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="inventors")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/inventors")
        else:
            messages.error(request, f"Failed to delete. Form is not valid!")
    return render(request, "app/address-book/inventors/delete.html", {"item": item, "form": form})


def inventors_update_view(request: HttpRequest, pk):
    item = Inventor.objects.get(id=pk)
    form = InventorForm(instance=item)
    if request.POST:
        form = InventorForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/inventors")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "inventors",
    }
    return render(request, "app/address-book/inventors/update.html", context)


# APPLICANT MODULE
def applicants_view(request):
    context = {
        "tabs": tabs,
        "active": "applicants",
        "items": Applicant.objects.all(),
        "form": ApplicantForm
    }
    return render(request, "app/address-book/applicants/applicants.html", context)


def applicants_detail_view(request: HttpRequest, pk):
    item = Applicant.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "applicants",
    }
    return render(request, "app/address-book/applicants/details.html", context)


# def applicants_create_view(request: HttpRequest):
#     form = ApplicantForm(initial=MultiValueDict(request.GET).dict())
#     if request.POST:
#         form = ApplicantForm(data=request.POST)
#         if form.is_valid():
#             attorney = form.save(commit=False)
#             attorney.type = 'Applicant'  # Set the value of 'type' here
#             attorney.save()
#             messages.success(request, "Item successfully created!")
#         else:
#             messages.error(request, f"Failed to create. Form is not valid!")
#     return HttpResponseRedirect("/app/address-book/applicants")

def applicants_create_view(request: HttpRequest):
    form = ApplicantForm(initial=MultiValueDict(request.GET).dict())
    if request.method == 'POST':
        form = ApplicantForm(data=request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.type = 'Applicant'  # Set the value of 'type' here
            applicant.surname = applicant.name
            applicant.save()
            print("saved now saving inventor")
            if form.cleaned_data['is_inventor']:
                Inventor.objects.create(
                    name=applicant.name,
                    surname=applicant.name,
                    phone=applicant.phone,
                    email=applicant.email,
                    nationality=applicant.nationality,
                    county_state=applicant.country_of_registration,
                    type = 'Inventor',
                    # Add other necessary fields from Applicant to Inventor
                    title=None,  # Provide appropriate value or leave as None
                    type_of_contract=None,  # Provide appropriate value or leave as None
                    employer_name=None,  # Provide appropriate value or leave as None
                    email_of_future_contact=applicant.email,

                    date_of_employment_termination=None,  # Provide appropriate value or leave as None
                    commencement_date=None,  # Provide appropriate value or leave as None



                    # employer_address_line_1=applicant.employer_address_line_1,  # Provide appropriate value or leave as None
                    # employer_address_line_2=applicant.employer_address_line_2,  # Provide appropriate value or leave as None
                    # employer_address_city=None,  # Provide appropriate value or leave as None
                    # employer_address_state=None,  # Provide appropriate value or leave as None
                    zip_postal_code=applicant.zip_postal_code,
                    notes=applicant.notes,
                    is_applicant=True
                )
            messages.success(request, "Item successfully created!")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/applicants")


def applicants_delete_view(request: HttpRequest, pk):
    item = Applicant.objects.get(id=pk)
    form = DeleteForm(module_name="applicants")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="applicants")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/applicants")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/applicants/delete.html", {"item": item, "form": form})


def applicants_update_view(request: HttpRequest, pk):
    item = Applicant.objects.get(id=pk)
    form = ApplicantForm(instance=item)
    if request.POST:
        form = ApplicantForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/applicants")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "applicants",
    }
    return render(request, "app/address-book/applicants/update.html", context)


### LICENSOR MODULE
def licensors_view(request):
    context = {
        "tabs": tabs,
        "active": "licensors",
        "items": Licensor.objects.all(),
        "form": LicensorForm
    }
    return render(request, "app/address-book/licensors/licensors.html", context)


def licensors_detail_view(request: HttpRequest, pk):
    item = Licensor.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "licensors",
    }
    return render(request, "app/address-book/licensors/details.html", context)


def licensors_create_view(request: HttpRequest):
    form = LicensorForm(initial=MultiValueDict(request.GET).dict())
    if request.method == 'POST':
        form = LicensorForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Licensor'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/licensors/")


def licensors_delete_view(request: HttpRequest, pk):
    item = Licensor.objects.get(id=pk)
    form = DeleteForm(module_name="licensors")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="licensors")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/licensors/")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/licensors/delete.html", {"item": item, "form": form})


def licensors_update_view(request: HttpRequest, pk):
    item = Licensor.objects.get(id=pk)
    form = LicensorForm(instance=item)
    if request.POST:
        form = LicensorForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/licensors")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "licensors",
    }
    return render(request, "app/address-book/licensors/update.html", context)


### LICENSEES MODULE
def licensees_view(request):
    context = {
        "tabs": tabs,
        "active": "licensees",
        "items": Licensee.objects.all(),
        "form": LicenseeForm
    }
    return render(request, "app/address-book/licensees/licensees.html", context)


def licensees_detail_view(request: HttpRequest, pk):
    item = Licensee.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "licensees",
    }
    return render(request, "app/address-book/licensees/details.html", context)


def licensees_create_view(request: HttpRequest):
    form = LicenseeForm(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = LicenseeForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Licensee'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/licensees/")


def licensees_delete_view(request: HttpRequest, pk):
    item = Licensee.objects.get(id=pk)
    form = DeleteForm(module_name="licensees")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="licensees")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/licensees/")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/licensees/delete.html", {"item": item, "form": form})


def licensees_update_view(request: HttpRequest, pk):
    item = Licensee.objects.get(id=pk)
    form = LicenseeForm(instance=item)
    if request.POST:
        form = LicenseeForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/licensees")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "licensees",
    }
    return render(request, "app/address-book/licensees/update.html", context)


### CONSULTANTS MODULE
def consultants_view(request):
    context = {
        "tabs": tabs,
        "active": "consultants",
        "items": Consultant.objects.all(),
        "form": ConsultantForm
    }
    return render(request, "app/address-book/consultants/consultants.html", context)


def consultants_detail_view(request: HttpRequest, pk):
    item = Consultant.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "consultants",
    }
    return render(request, "app/address-book/consultants/details.html", context)


def consultants_create_view(request: HttpRequest):
    form = ConsultantForm(initial=MultiValueDict(request.GET).dict())
    if request.method == 'POST':
        form = ConsultantForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Consultant'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/consultants")


def consultants_delete_view(request: HttpRequest, pk):
    item = Consultant.objects.get(id=pk)
    form = DeleteForm(module_name="consultants")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="consultants")
        if form.is_valid():
            item.delete()
            return HttpResponseRedirect("/app/address-book/consultants")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/consultants/delete.html", {"item": item, "form": form})


def consultants_update_view(request: HttpRequest, pk):
    item = Consultant.objects.get(id=pk)
    form = ConsultantForm(instance=item)
    if request.POST:
        form = ConsultantForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/consultants")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "consultants",
    }
    return render(request, "app/address-book/consultants/update.html", context)


### Associate MODULE
def Associates_view(request):
    context = {
        "tabs": tabs,
        "active": "Associates",
        "items": Associate.objects.all(),
        "form": AssociateForm
    }
    return render(request, "app/address-book/agents/agents.html", context)


def Associates_detail_view(request: HttpRequest, pk):
    item = Associate.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "Associates",
    }
    return render(request, "app/address-book/Associates/details.html", context)


def Associates_create_view(request: HttpRequest):
    form = AssociateForm(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = AssociateForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Associate'  # Set the value of 'type' here
            attorney.surname = attorney.name
            attorney.save()
            messages.success(request, "Item successfully created!")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/Associates")


def Associates_delete_view(request: HttpRequest, pk):
    item = Associate.objects.get(id=pk)
    form = DeleteForm(module_name="Associates")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="Associates")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/Associates")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/agents/delete.html", {"item": item, "form": form})


def associates_update_view(request: HttpRequest, pk):
    item = Associate.objects.get(id=pk)
    form = AssociateForm(instance=item)
    if request.POST:
        form = AssociateForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/Associates")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "Associates",
    }
    return render(request, "app/address-book/agents/update.html", context)


### PARALEGALS MODULE
def paralegals_view(request):
    context = {
        "tabs": tabs,
        "active": "paralegals",
        "items": Paralegal.objects.all(),
        "form": ParalegalForm
    }
    return render(request, "app/address-book/paralegals/paralegals.html", context)


def paralegals_detail_view(request: HttpRequest, pk):
    item = Paralegal.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "paralegals",
    }
    return render(request, "app/address-book/paralegals/details.html", context)


def paralegals_create_view(request: HttpRequest):
    form = ParalegalForm(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = ParalegalForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Paralegal'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
            return HttpResponseRedirect("/app/address-book/paralegals")
        messages.error(request, f"Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/paralegals")


def paralegals_delete_view(request: HttpRequest, pk):
    item = Paralegal.objects.get(id=pk)
    form = DeleteForm(module_name="paralegals")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="paralegals")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/paralegals")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/paralegals/delete.html", {"item": item, "form": form})


def paralegals_update_view(request: HttpRequest, pk):
    item = Paralegal.objects.get(id=pk)
    form = ParalegalForm(instance=item)
    if request.POST:
        form = ParalegalForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/paralegals")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "paralegals",
    }
    return render(request, "app/address-book/paralegals/update.html", context)


### ATTORNY MODULE
def attorneys_view(request):
    context = {
        "tabs": tabs,
        "active": "attorneys",
        "items": Attorney.objects.all(),
        "form": AttorneyForm
    }
    return render(request, "app/address-book/attorneys/attorneys.html", context)


def attorneys_detail_view(request: HttpRequest, pk):
    item = Attorney.objects.get(id=pk)
    context = {
        "tabs": tabs,
        "item": item,
        "active": "attorneys",
    }
    return render(request, "app/address-book/attorneys/details.html", context)


def attorneys_create_view(request: HttpRequest):
    form = AttorneyForm(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = AttorneyForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.type = 'Attorney'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")

        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return HttpResponseRedirect("/app/address-book/attorneys")


def attorneys_delete_view(request: HttpRequest, pk):
    item = Attorney.objects.get(id=pk)
    form = DeleteForm(module_name="attorneys")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="attorneys")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/attorneys")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/attorneys/delete.html", {"item": item, "form": form})


def attorneys_update_view(request: HttpRequest, pk):
    item = Attorney.objects.get(id=pk)
    form = AttorneyForm(instance=item)
    if request.POST:
        form = AttorneyForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/attorneys")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "attorneys",
    }
    return render(request, "app/address-book/attorneys/update.html", context)


def other_provider_view(request):
    context = {
        "tabs": tabs,
        "active": "other_provider",
        "items": OtherProvider.objects.all(),
        "form": OtherProviderForm
    }
    return render(request, "app/address-book/attorneys/other.html", context)


def create_other_provider(request: HttpRequest):
    if request.method == 'POST':
        form = OtherProviderForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.name = attorney.contact_person  # Assuming contact_person is meant to be used as the name
            attorney.type = 'OtherProvider'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
            return HttpResponseRedirect("/app/address-book/other_provider")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    else:
        form = OtherProviderForm(initial=MultiValueDict(request.GET).dict())

    return HttpResponseRedirect("/app/address-book/other_provider")



def costcenter_create_view(request: HttpRequest):
    if request.method == 'POST':
        form = CostCenterForm(data=request.POST)
        if form.is_valid():
            attorney = form.save(commit=False)
            attorney.surname = attorney.name  # Assuming contact_person is meant to be used as the name
            attorney.type = 'CostCenter'  # Set the value of 'type' here
            attorney.save()
            messages.success(request, "Item successfully created!")
            return HttpResponseRedirect("/app/address-book/costcenter")
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Failed to create. Form is not valid!")
    else:
        form = OtherProviderForm(initial=MultiValueDict(request.GET).dict())

    return HttpResponseRedirect("/app/address-book/costcenter")


def costcenter_view(request):
    context = {
        "tabs": tabs,
        "active": "costcenter",
        "items": CostCenter.objects.all(),
        "form": CostCenterForm
    }
    return render(request, "app/address-book/costcenter/create.html", context)


def costcenter_delete_view(request: HttpRequest, pk):
    item = Attorney.objects.get(id=pk)
    form = DeleteForm(module_name="coscenter")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="costcenter")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/address-book/costcenter")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/address-book/costcenter/delete.html", {"item": item, "form": form})


def costcenter_update_view(request: HttpRequest, pk):
    item = CostCenter.objects.get(id=pk)
    form = CostCenterForm(instance=item)
    if request.POST:
        form = AttorneyForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/address-book/costcenter")
        else:
            messages.error(request, f"Failed to update. Form is not valid!")
    context = {
        "tabs": tabs,
        "item": item,
        "form": form,
        "active": "attorneys",
    }
    return render(request, "app/address-book/costcenter/update.html", context)
