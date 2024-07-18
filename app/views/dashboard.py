from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.datastructures import MultiValueDict
from django.shortcuts import render
from django.db.models import Q
from itertools import chain
from difflib import SequenceMatcher
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
    form = HomeSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        title = form.cleaned_data.get('title')
        primary_attorney = form.cleaned_data.get('primary_attorney')
        secondary_attorney = form.cleaned_data.get('secondary_attorney')
        type_of_filing = form.cleaned_data.get('type_of_filing')
        status = form.cleaned_data.get('status')
        Associates = form.cleaned_data.get('Associates')
        Associate_refs = form.cleaned_data.get('Associate_refs')

        # Perform the database query using the provided search parameters
        queryset = Family.objects.none()
        if title:
            queryset |= Family.objects.filter(titles__icontains=title)
        if primary_attorney:
            queryset |= Family.objects.filter(primary_attorney__icontains=primary_attorney)
        if secondary_attorney:
            queryset |= Family.objects.filter(secondary_attorney__icontains=secondary_attorney)
        if type_of_filing:
            queryset |= Family.objects.filter(type_of_filing__icontains=type_of_filing)
        if status:
            queryset |= Family.objects.filter(status__icontains=status)
        if Associates:
            queryset |= Family.objects.filter(_Associates__icontains=Associates)
        if Associate_refs:
            queryset |= Family.objects.filter(_Associate_refs__icontains=Associate_refs)

        results = list(queryset)

        if not results:
                form.add_error(None, "Search not found")

        

    context = {'form': form, 'results': results}
    print(context)
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