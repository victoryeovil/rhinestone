import json
from app import data
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.http.request import HttpRequest
from django.contrib import messages
from django.utils.datastructures import MultiValueDict
from app.forms.modules import PatentForms, PatentPCTForm
from app.models import (
    Trademark,
    Patent,
    Family,
    Design,
)
from app.forms import (
    DeleteForm,
    TrademarkForm,
    PatentForm,
    FamilyForm,
    DesignForm,FamilyDesignForm,FamilyPatentForm,FamilyTrademarkForm
)
from app.functions.generate_id import generate_id
from app.models.contacts import Applicant, Inventor
from app.models.modules import Country


# FAMILIES MODULE
def families_list_view(request: HttpRequest):
    return render(request, "app/modules/families/list.html", {"items": Family.objects.all()})


def families_detail_view(request: HttpRequest, pk):
    return render(request, "app/modules/families/details.html", {"item": Family.objects.get(id=pk)})





def families_create_view(request,form,form_p,modal):
    
    form=form
    if request.POST: 
        type_of_filing = (request.POST.get('submit')) 
        form = form_p(data=request.POST)
        if form.is_valid():
            family = form.save()
            messages.success(request, f"Item successfully created!")
            data = form.data.dict()
            if type_of_filing == "Trademark" :
                content = {"secondary_paralegal": data['secondary_paralegal'],"country": data['country'],
                        "primary_paralegal": data['primary_paralegal'], 'secondary_attorney': data['secondary_attorney'],
                        'primary_attorney': data['primary_attorney'], "type_of_filing": type_of_filing , 'family' :  family.id}
                request.session['Trademark'] =  content 
                return HttpResponseRedirect("/app/modules/trademarks/add/")
            elif type_of_filing == "Design" : 
                content = {"internal_title": data['internal_title'], "formal_title": data['formal_title'],"country": data['country'], 
                                                                       "secondary_paralegal": data['secondary_paralegal'], "primary_paralegal": data['primary_paralegal'],
                                                                         'secondary_attorney': data['secondary_attorney'],'primary_attorney': data['primary_attorney'],
                                                                        'cost_centre_code': data['cost_centre_code'], 'licencor': data['licensor'],
                                                                         'licence': data['licenced'] ,  'cost_centre' :data['cost_centre'] , 'status' :data['sub_status'], "type_of_filing": type_of_filing , 'family' :  family.id}
                request.session['Design'] =  content 
                return HttpResponseRedirect("/app/modules/designs/add/")
            elif type_of_filing == "Patent" : 
                content = {"internal_title":  data['internal_title'], "formal_title": data['formal_title'], 
                                                                        'cost_centre_code': data['cost_centre_code'],  'licence':data['licenced'],  
                                                                        'primary_attorney':data['primary_attorney'], 'secondary_attorney' :  data['secondary_attorney']
                                                                        ,'primary_paralegal' : data['primary_paralegal'] , 'secondary_paralegal' : data['secondary_paralegal'],
                                                                        "type_of_filing": type_of_filing , 'family' : family.id}
                request.session['Patent'] =  content                 
                return HttpResponseRedirect("/app/modules/patents/add/") 
            else:
                return HttpResponseRedirect("/app/modules/families/list/")
        messages.error(request, f"Failed to create. Form is not valid!")
    return render(request, "app/modules/families/create.html", {"form": form,'modal':modal}) 

def families_create_patent_view(request: HttpRequest):
    form = FamilyPatentForm(initial=MultiValueDict(request.GET).dict())
    form_p = FamilyPatentForm()
    modal = PatentPCTForm()  # Instantiate the PatentPCTForm

    return families_create_view(request, form, form_p, modal)

def families_create_design_view(request: HttpRequest):
     form = FamilyDesignForm(initial=MultiValueDict(request.GET).dict())
     form_p=FamilyDesignForm
     modal = PatentPCTForm()
     return families_create_view(request,form,form_p,modal)

def families_create_trademark_view(request: HttpRequest):
     form = FamilyTrademarkForm(initial=MultiValueDict(request.GET).dict())
     form_p=FamilyTrademarkForm
     modal = PatentPCTForm()
     return families_create_view(request,form,form_p,modal)

def families_delete_view(request: HttpRequest, pk):
    item = Family.objects.get(id=pk)
    form = DeleteForm(module_name="families")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="families")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/modules/families/list/")
        messages.error(request, f"Failed to delete. Form is not valid!")
    return render(request, "app/modules/families/delete.html", {"item": item, "form": form})


def families_update_view(request: HttpRequest, pk):
    item = Family.objects.get(id=pk)
    form = FamilyForm(instance=item)
    forms = PatentPCTForm()
    if request.POST:
        form = FamilyForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            data = form.data.dict()
            type_of_filing = (request.POST.get('submit')) 
            messages.success(request, f"Item successfully updated!")
            if type_of_filing == "Trademark" :
                content = {"secondary_paralegal": data['secondary_paralegal'],
                        "primary_paralegal": data['primary_paralegal'], 'secondary_attorney': data['secondary_attorney'],
                        'primary_attorney': data['primary_attorney'], "type_of_filing": type_of_filing }
                request.session['Trademark'] =  content
                return HttpResponseRedirect("/app/modules/trademarks/add/")
            elif type_of_filing == "Design" : 
                content = {"internal_title": data['internal_title'], "formal_title": data['formal_title'], 
                                                                       "secondary_paralegal": data['secondary_paralegal'], "primary_paralegal": data['primary_paralegal'],
                                                                         'secondary_attorney': data['secondary_attorney'],'primary_attorney': data['primary_attorney'],
                                                                        'cost_centre_code': data['cost_centre_code'], 'licencor': data['licensor'],
                                                                         'licence': data['licenced'] ,  'cost_centre' :data['cost_centre'] , 'status' :data['sub_status'], "type_of_filing": type_of_filing}
                request.session['Design'] =  content 
                return HttpResponseRedirect("/app/modules/designs/add/")
            elif type_of_filing == "Patent" : 
                content = {"internal_title":  data['internal_title'], "formal_title": data['formal_title'], 
                                                                        'cost_centre_code': data['cost_centre_code'],  'licence':data['licenced'],  
                                                                        'primary_attorney':data['primary_attorney'], 'secondary_attorney' :  data['secondary_attorney']
                                                                        ,'primary_paralegal' : data['primary_paralegal'] , 'secondary_paralegal' : data['secondary_paralegal'],
                                                                        "type_of_filing": type_of_filing}
                request.session['Patent'] =  content                 
                return HttpResponseRedirect("/app/modules/patents/add/")
            else:
                return HttpResponseRedirect("/app/modules/families/list/")
        messages.error(request, f"Failed to update. Form is not valid!")
    return render(request, "app/modules/families/update.html", {"item": item, "form": form, "modal":forms})


# PATENTS MODULE
def patents_list_view(request: HttpRequest):
    return render(request, "app/modules/patents/list.html", {"items": Patent.objects.all()})


def patents_detail_view(request: HttpRequest, pk):
    return render(request, "app/modules/patents/details.html", {"item": Patent.objects.get(id=pk)})

def patent_pct_form_view(request):
    form = PatentPCTForm()
    return render(request, 'app/modules/patents/patent_pct_form.html', {'form': form})

def patents_create_view(request):
    url_initial = {}
    
    if 'country' in request.GET:
        url_initial = MultiValueDict(request.GET).dict()
        country_name = url_initial.get("country")
        family_name = url_initial.get("internal_title")
        print(family_name)
        
        country_code = next((country["code"] for country in data.countries.PCT_COUNTRIES if country["name"] == country_name), None)
        if country_code:
            url_initial["country"] = [country_code]
            url_initial['family'] = [family_name]
            

    if request.method == 'GET':
        # Populate form fields using URL parameters
        family_data = {
            "case_no": url_initial.get("case_no"),
            "internal_title": url_initial.get("internal_title"),
            "formal_title": url_initial.get("formal_title"),
            "sub_filing_type": url_initial.get("sub_filing_type"),
        }
        initial_data = {**family_data, **url_initial}
    else:
        initial_data = url_initial

    form = PatentForm(initial=initial_data)

    if request.method == 'POST':
        form = PatentForm(data=request.POST)
        session_initial = MultiValueDict(request.POST).dict()
        print(form)

    if request.method == 'POST':
        form = PatentForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully created!")
            return HttpResponseRedirect("/app/modules/patents/list/")
        else:
            messages.error(request, f"Failed to create. Form is not valid!")

    patent = Patent.objects.all()  # Fetch all items from the Patent model

    content = {
        'form': form,
        'designs': patent,  # Pass the designs queryset to the template
    }
    return render(request, "app/modules/patents/create.html", content)


def patents_create_views(request: HttpRequest):
    if (request.session['Patent']!={}):
        form =PatentForm(initial=MultiValueDict(request.session['Patent']))
        #print(request.session['Patent']["country"])
    else:

        form = PatentForms(initial=MultiValueDict(request.GET).dict())
    if request.POST:
        form = PatentForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully created!")
            return HttpResponseRedirect("/app/modules/patents/list/")
        messages.error(request, f"Failed to create. Form is not valid!")
        # print(form.errors)
    content = request.session.get('Patent' , {})
    request.session['Patent'] = {}
    patent = Patent.objects.all()  # Fetch all items from the Design model

    content = {
        'form': form,
        'designs': patent,  # Pass the designs queryset to the template
    }
    return render(request, "app/modules/patents/create.html", content)

def inventor_autocomplete(request):
    query = request.GET.get('query', '')  # Get the user's input from the query parameter
    inventors = Inventor.objects.filter(surname__icontains=query)[:10]  # Retrieve matching inventors

    # Create a list of dictionaries with inventor data
    inventor_data = []
    for inventor in inventors:
        inventor_info = {
            'id': inventor.id,
            'surname': inventor.surname,
            'name': inventor.name,
            'nationality': inventor.nationality,
            'employer_name': inventor.employer_name,
            # Add more fields here as needed
        }
        inventor_data.append(inventor_info)
        print(inventor_data)

    return JsonResponse({'suggestions': inventor_data})
def applicant_autocomplete(request):
    query = request.GET.get('query', '')  # Get the user's input from the query parameter
    inventors = Applicant.objects.filter(surname__icontains=query)[:10]  # Retrieve matching inventors

    # Create a list of dictionaries with inventor data
    applicant_data = []
    for inventor in inventors:
        inventor_info = {
            'id': inventor.id,
            'surname': inventor.surname,
            'name': inventor.name,
            'nationality': inventor.nationality,
            'employer_name': inventor.notes,
            # Add more fields here as needed
        }
        applicant_data.append(inventor_info)
        print(applicant_data)

    return JsonResponse({'suggestion': applicant_data})

def patents_delete_view(request: HttpRequest, pk):
    item = Patent.objects.get(id=pk)
    form = DeleteForm(module_name="patents")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="patents")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/modules/patents/list/")
        messages.error(request, f"Failed to delete. Form is not valid!")
    return render(request, "app/modules/patents/delete.html", {"item": item, "form": form})


def patents_update_view(request: HttpRequest, pk):
    item = Patent.objects.get(id=pk)
    form = PatentForm(instance=item)
    if request.POST:
        form = PatentForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/modules/patents/list/")
        messages.error(request, f"Failed to update. Form is not valid!")
    return render(request, "app/modules/patents/update.html", {"item": item, "form": form})


# DESIGNS MODULE
def designs_list_view(request: HttpRequest):
    return render(request, "app/modules/designs/list.html", {"items": Design.objects.all()})


def designs_detail_view(request: HttpRequest, pk):
    return render(request, "app/modules/designs/details.html", {"item": Design.objects.get(id=pk)})


def designs_create_view(request: HttpRequest):
    if 'Design' in request.session and request.session['Design'] != {}:
        form = DesignForm(initial=MultiValueDict(request.session['Design']))
        print(request.session['Design']["country"])
    else:
        form = DesignForm(initial=MultiValueDict(request.GET).dict())

    if request.method == 'POST':
        form = DesignForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item successfully created!")
            return HttpResponseRedirect("/app/modules/designs/list/")
        else:
            messages.error(request, "Failed to create. Form is not valid!")
            messages.error(request, form.errors.as_ul())

    content = {
        'form': form,
        'designs': Design.objects.all(),  # Fetch all items from the Design model
    }

    print(content)
    return render(request, "app/modules/designs/create.html", content)


def designs_delete_view(request: HttpRequest, pk):
    item = Design.objects.get(id=pk)
    form = DeleteForm(module_name="designs")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="designs")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/modules/designs/list/")
        messages.error(request, f"Failed to delete. Form is not valid!")
    return render(request, "app/modules/designs/delete.html", {"item": item, "form": form})


def designs_update_view(request: HttpRequest, pk):
    item = Design.objects.get(id=pk)
    form = DesignForm(instance=item)
    if request.POST:
        form = TrademarkForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/modules/designs/list/")
        messages.error(request, f"Failed to update. Form is not valid!")
    return render(request, "app/modules/designs/update.html", {"item": item, "form": form})

# TRADEMARKS MODULE


def trademarks_list_view(request: HttpRequest):
    return render(request, "app/modules/trademarks/list.html", {"items": Trademark.objects.all()})


def trademarks_detail_view(request: HttpRequest, pk):
    return render(request, "app/modules/trademarks/details.html", {"item": Trademark.objects.get(id=pk)})


def trademarks_create_view(request: HttpRequest):
    if 'Trademark' in request.session and request.session['Trademark'] != {}:
        form = TrademarkForm(initial=MultiValueDict(request.session['Trademark']))
        print(request.session['Trademark']["country"])
    else:
        form = TrademarkForm(initial=MultiValueDict(request.GET).dict())

    if request.method == 'POST':
        form = TrademarkForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item successfully created!")
            return HttpResponseRedirect("/app/modules/trademarks/list/")
        else:
            messages.error(request, "Failed to create. Form is not valid!")

    content = {
        'form': form,
        'trademarks': Trademark.objects.all(),  # Fetch all items from the Trademark model
    }

    return render(request, "app/modules/trademarks/create.html", content)


def trademarks_delete_view(request: HttpRequest, pk):
    item = Trademark.objects.get(id=pk)
    form = DeleteForm(module_name="trademarks")
    if request.POST:
        form = DeleteForm(data=request.POST, module_name="trademarks")
        if form.is_valid():
            item.delete()
            messages.success(request, f"Item successfully deleted!")
            return HttpResponseRedirect("/app/modules/trademarks/list/")
        messages.error(request, f"Failed to delete. Form is not valid!")
    return render(request, "app/modules/trademarks/delete.html", {"item": item, "form": form})


def trademarks_update_view(request: HttpRequest, pk):
    item = Trademark.objects.get(id=pk)
    form = TrademarkForm(instance=item)
    if request.POST:
        form = TrademarkForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item successfully updated!")
            return HttpResponseRedirect("/app/modules/trademarks/list/")
        messages.error(request, f"Failed to update. Form is not valid!")
    return render(request, "app/modules/trademarks/update.html", {"item": item, "form": form})



def intellectual_property_view(request):
    family_data = Family.objects.all().values('id', 'family_no', 'titles', 'official_numbers')
    patent_data = Patent.objects.all().values('id', 'titles', 'agent', 'agent_ref', 'type_of_filing', 'official_numbers')
    design_data = Design.objects.all().values('id', 'titles', 'agent', 'agent_ref', 'type_of_filing', 'official_numbers')

    combined_data = list(family_data) + list(patent_data) + list(design_data)

    context = {
        'intellectual_property': combined_data
    }

    return render(request, 'app/modules/intellectual_property.html', context)


def related_cases_view(request):
    if request.method == "POST":
        family_case_number = request.POST.get("family_case_number")
        print(family_case_number)
        related_cases = Patent.objects.all()
        print(related_cases)
        related_cases_data = []

        for case in related_cases:
            related_cases_data.append({
                "case_number": case.case_no,
                "country": case.country,
                "application_number": case.priority_provisional_application_no,
                "application_date": case.priority_provisional_date,
                "inventors": ", ".join(str(inventor) for inventor in case.inventor.all())
            })
        print(related_cases_data)
        return JsonResponse({"related_cases": related_cases_data})

    return render(request, "modules/families/create.html") 

