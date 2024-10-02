from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.datastructures import MultiValueDict
from django.shortcuts import render
from django.db.models import Q, ForeignKey
from itertools import chain
from difflib import SequenceMatcher
from django.core.exceptions import FieldDoesNotExist
from app.models import (
    Family, Patent, Trademark, Design, BaseModel,
    User, Contact, InventionDisclosure, Invoice
)
# from app.forms.modules import QuickSearchForm
from app.forms.quick_search import QuickSearchForm, HomeSearchForm


from difflib import SequenceMatcher

def home_search_view(request):
    form = QuickSearchForm(request.GET or None)
    results = []

    if request.method == 'POST':
        form = QuickSearchForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            query = cleaned_data.get('query')

            patent_results = Patent.objects.none()
            trademark_results = Trademark.objects.none()
            family_results = Family.objects.none()
            design_results = Design.objects.none()

            if query:
                # Perform the search based on the query
                patent_results = Patent.objects.filter(Q(_titles__icontains=query) | Q(official_numbers__icontains=query))
                trademark_results = Trademark.objects.filter(titles__icontains=query)
                family_results = Family.objects.filter(titles__icontains=query)
                design_results = Design.objects.filter(titles__icontains=query)

            # Perform the search based on other form fields
            official_numbers = cleaned_data.get('_official_numbers__icontains')
            if official_numbers:
                patent_results |= Patent.objects.filter(official_numbers__icontains=official_numbers)

            titles = cleaned_data.get('_titles__icontains')
            if titles:
                patent_results |= Patent.objects.filter(titles__icontains=titles)

            primary_attorney = cleaned_data.get('primary_attorney')
            if primary_attorney:
                patent_results |= Patent.objects.filter(primary_attorney=primary_attorney)

            secondary_attorney = cleaned_data.get('secondary_attorney')
            if secondary_attorney:
                patent_results |= Patent.objects.filter(secondary_attorney=secondary_attorney)

            type_of_filing = cleaned_data.get('type_of_filing')
            if type_of_filing:
                patent_results |= Patent.objects.filter(type_of_filing=type_of_filing)

            Associates = cleaned_data.get('_Associates')
            if Associates:
                patent_results |= Patent.objects.filter(Associates=Associates)

            Associate_refs = cleaned_data.get('_Associate_refs')
            if Associate_refs:
                patent_results |= Patent.objects.filter(Associate_refs=Associate_refs)

            status__in = cleaned_data.get('status__in')
            if status__in:
                patent_results |= Patent.objects.filter(status__in=status__in)

            results = list(chain(patent_results, trademark_results, family_results, design_results))

            if not results:
                form.add_error(None, "Search not found")

    return render(request, 'app/home.html', {'form': form, 'result': results})



def home_view(request):
    form = HomeSearchForm(request.POST or None)
    results = []

    if form.is_valid():
        # Extract form data
        form_data = {
            'title': form.cleaned_data.get('title'),
            'primary_attorney': form.cleaned_data.get('primary_attorney'),
            'secondary_attorney': form.cleaned_data.get('secondary_attorney'),
            'associate': form.cleaned_data.get('associate'),
            'instructor': form.cleaned_data.get('instructor'),
            'owner': form.cleaned_data.get('owner'),
            'name': form.cleaned_data.get('name'),
            'primary_paralegal': form.cleaned_data.get('primary_paralegal'),
            'secondary_paralegal': form.cleaned_data.get('secondary_paralegal'),
            'inventor': form.cleaned_data.get('inventor'),
            'case_reference': form.cleaned_data.get('case_reference'),
            'family': form.cleaned_data.get('family'),
            'official_number': form.cleaned_data.get('official_number'),
            'instructor_reference': form.cleaned_data.get('instructor_reference'),
            'associate_refs': form.cleaned_data.get('Associate_refs'),
            'priority_provisional_application_no': form.cleaned_data.get('priority_provisional_application_no'),
            'pct_application_no': form.cleaned_data.get('pct_application_no'),
            'application_no': form.cleaned_data.get('application_no'),
            'publication_no': form.cleaned_data.get('publication_no'),
            'grant_number': form.cleaned_data.get('grant_number'),
            'registration_no': form.cleaned_data.get('registration_no'),
            'case_office': form.cleaned_data.get('case_office'),
            'case_type': form.cleaned_data.get('case_type'),
            'country': form.cleaned_data.get('country'),
            'property_type': form.cleaned_data.get('property_type'),
            'case_category': form.cleaned_data.get('case_category'),
            'sub_type': form.cleaned_data.get('sub_type'),
            'basis': form.cleaned_data.get('basis'),
            'case_class': form.cleaned_data.get('case_class'),
            'classes': form.cleaned_data.get('classes'),
            'status': form.cleaned_data.get('status__in'),
            'case_status': form.cleaned_data.get('case_status'),
            'renewal_status': form.cleaned_data.get('renewal_status'),
            'keyword': form.cleaned_data.get('keyword'),
            'type_of_mark': form.cleaned_data.get('type_of_mark'),
        }

        # Helper function to get all fields from the model
        def get_model_fields(model):
            return [field.name for field in model._meta.get_fields()]

        # Helper function to build filters for a specific model based on matching fields
        def apply_filters(queryset, model):
            model_filters = Q()
            model_fields = get_model_fields(model)
            matching_fields = []

           
            for field, value in form_data.items():
                if value and field in model_fields:
                    matching_fields.append(field)
                    # print(f"Field '{field}' found in {model.__name__}, applying filter.")

            for field in matching_fields:
                value = form_data[field]
                try:
                    model_field = model._meta.get_field(field)

                    if isinstance(model_field, ForeignKey):
                       
                        related_field_name = f'{field}__id'
                        model_filters &= Q(**{related_field_name: value.id})
                        print(f"ForeignKey filter applied: {related_field_name} with value {value.id}")
                    else:
                        model_filters &= Q(**{f'{field}__icontains': value})
                        # print(f"Filter applied for field: {field} with value: {value}")

                except FieldDoesNotExist:
                    print(f"Field '{field}' does not exist in {model.__name__}, skipping.")

            return queryset.filter(model_filters)

        # Debugging: Print out the type of filing
        type_of_filing = form.cleaned_data.get('type_of_filing')
        print(f"Checking the type of filing: {type_of_filing}")

        # Apply filters for each model, dynamically checking field existence
        if type_of_filing == "Design":
            results = list(apply_filters(Design.objects.all(), Design))
        elif type_of_filing == "Patent":
            results = list(apply_filters(Patent.objects.all(), Patent))
        elif type_of_filing == "Trademark":
            results = list(apply_filters(Trademark.objects.all(), Trademark))
        else:
            # If no specific type_of_filing is selected, search in all models
            results = list(chain(
                apply_filters(Design.objects.all(), Design),
                apply_filters(Patent.objects.all(), Patent),
                apply_filters(Trademark.objects.all(), Trademark)
            ))

        # Debugging: Print the number of results found
        if not results:
            form.add_error(None, "No records found based on your search criteria.")
            print("No records found based on the search criteria.")
        else:
            print(f'Found {len(results)} result(s).')

    context = {'form': form, 'results': results}
    return render(request, 'app/home_search_view.html', context)


@login_required( login_url="/login/")
def dashboard_view(request):
    context = {
        "users_count": User.objects.count(),
        "contacts_count": Contact.objects.count(),
        "invoices_count": Invoice.objects.count(),
        "invention_disclosures_count": InventionDisclosure.objects.count(),
        "quick_insight": [
            {"name": "Patent", "count": 10},
        ],
         "quick_insight1": [
            {"name": "Trade Mark", "count": 15},
        ],
         "quick_insight2": [
            {"name": "Design", "count": 12},
        ],
         "quick_insight3": [
           {"name": "Family", "count": 40}, 
        ]

    }
    return render(request, "app/dashboard.html", context)

@login_required( login_url="/login/")
def coming_soon_view(request):
    return render(request, "app/coming_soon.html")

@login_required( login_url="/login/")
def page_not_found_view(request, exception=None):
    return render(request, "app/error.html", {
        "subject": "Page not found!",
        "code": 404,
        "msg": "The requested view was not found!"
    })

def new_dash(request):
    return render(request, 'app/landing_page.html')


def search_view(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    results = []

    if query:
        if category == 'text':
            family_results = Family.objects.filter(internal_title__icontains=query)
            patent_results = Patent.objects.filter(internal_title__icontains=query)
            design_results = Design.objects.filter(internal_title__icontains=query)
            trademark_results = Trademark.objects.filter(internal_title__icontains=query)
        elif category == 'contacts':
            family_results = Family.objects.filter(applicant__name__icontains=query)
            patent_results = Patent.objects.filter(inventor__name__icontains=query)
            design_results = Design.objects.filter(licensor__name__icontains=query)
            trademark_results = Trademark.objects.filter(associate__name__icontains=query)
        elif category == 'official_numbers':
            family_results = Family.objects.filter(family_no__icontains=query)
            patent_results = Patent.objects.filter(case_no__icontains=query)
            design_results = Design.objects.filter(case_no__icontains=query)
            trademark_results = Trademark.objects.filter(case_no__icontains=query)
        elif category == 'modules':
            patent_results = Patent.objects.filter(case_no__icontains=query)
            design_results = Design.objects.filter(case_no__icontains=query)
            trademark_results = Trademark.objects.filter(case_no__icontains=query)

        # Collect results from all models
        results = list(family_results) + list(patent_results) + list(design_results) + list(trademark_results)

    return render(request, 'app/search_results.html', {'results': results})