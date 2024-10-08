from django.urls import path

from app.views import (
    dashboard,
    files,
    contacts,
    billing,
    inventions,
    modules
)
from app.views.contacts_crud import contact_detail_view, contact_edit_view, contact_delete_view

urlpatterns = [
    # ADMIN VIEWS
    path("landing/", dashboard.home_view, name="dashboard"),
    path("dashboard/", dashboard.dashboard_view),
    path('', dashboard.new_dash, name="landing"),
    path('search_view', dashboard.search_view, name="search_view"),
    # Files
    path("file/upload/", files.upload_file),  # file.upload),
    # ADDRESS BOOK
    path("address-book/contacts/", contacts.contacts_view, name="contacts"),
    path('contacts/<str:model_name>/<int:pk>/', contact_detail_view, name='contact_detail'),
    path('contacts/<str:model_name>/<int:pk>/edit/', contact_edit_view, name='contact_edit'),
    path('contacts/<str:model_name>/<int:pk>/delete/', contact_delete_view, name='contact_delete'),
    # other provider
    path("address-book/other_provider/", contacts.other_provider_view),
    path("address-book/other_provider/add/", contacts.create_other_provider),
    # contacts.inventors_view),
    path("address-book/inventors/", contacts.inventors_view),
    path("address-book/inventors/add/", contacts.inventors_create_view),
    path("address-book/inventors/detail/<int:pk>/",
         contacts.inventors_detail_view),
    path("address-book/inventors/edit/<int:pk>/",
         contacts.inventors_update_view),
    path("address-book/inventors/delete/<int:pk>/",
         contacts.inventors_delete_view),
    # contacts.applicants_view),
    path("address-book/applicants/", contacts.applicants_view),
    path("address-book/applicants/add/", contacts.applicants_create_view),
    path("address-book/applicants/detail/<int:pk>/",
         contacts.applicants_detail_view),
    path("address-book/applicants/edit/<int:pk>/",
         contacts.applicants_update_view),
    path("address-book/applicants/delete/<int:pk>/",
         contacts.applicants_delete_view),
    # contacts.licensors_view),
    path("address-book/licensors/", contacts.licensors_view),
    path("address-book/licensors/add/", contacts.licensors_create_view),
    path("address-book/licensors/detail/<int:pk>/",
         contacts.licensors_detail_view),
    path("address-book/licensors/edit/<int:pk>/",
         contacts.licensors_update_view),
    path("address-book/licensors/delete/<int:pk>/",
         contacts.licensors_delete_view),
    # contacts.licensees_view),
    path("address-book/licensees/", contacts.licensees_view),
    path("address-book/licensees/add/", contacts.licensees_create_view),
    path("address-book/licensees/detail/<int:pk>/",
         contacts.licensees_detail_view),
    path("address-book/licensees/edit/<int:pk>/",
         contacts.licensees_update_view),
    path("address-book/licensees/delete/<int:pk>/",
         contacts.licensees_delete_view),
    # contacts.consultants_view),
    path("address-book/consultants/", contacts.consultants_view),
    path("address-book/consultants/add/", contacts.consultants_create_view),
    path("address-book/consultants/detail/<int:pk>/", contacts.consultants_detail_view),
    path("address-book/consultants/edit/<int:pk>/", contacts.consultants_update_view),
    path("address-book/consultants/delete/<int:pk>/", contacts.consultants_delete_view),

    # contacts.Associates_view),
    path("address-book/Associates/", contacts.Associates_view),
    path("address-book/Associates/add/", contacts.Associates_create_view),
    path("address-book/Associates/detail/<int:pk>/", contacts.Associates_detail_view),
    path("address-book/Associates/edit/<int:pk>/", contacts.associates_update_view),
    path("address-book/Associates/delete/<int:pk>/", contacts.Associates_delete_view),
    # contacts.paralegals_view),
    path("address-book/paralegals/", contacts.paralegals_view),
    path("address-book/paralegals/add/", contacts.paralegals_create_view),
    path("address-book/paralegals/detail/<int:pk>/", contacts.paralegals_detail_view),
    path("address-book/paralegals/edit/<int:pk>/", contacts.paralegals_update_view),
    path("address-book/paralegals/delete/<int:pk>/", contacts.paralegals_delete_view),
    # contacts.attorneys_view),
    path("address-book/attorneys/", contacts.attorneys_view),
    path("address-book/attorneys/add/", contacts.attorneys_create_view),
    path("address-book/attorneys/detail/<int:pk>/", contacts.attorneys_detail_view),
    path("address-book/attorneys/edit/<int:pk>/", contacts.attorneys_update_view),
    path("address-book/attorneys/delete/<int:pk>/", contacts.attorneys_delete_view),

    #contacts.costcenter
    path("address-book/costcenter/add/", contacts.costcenter_create_view),
    path("address-book/costcenter/", contacts.costcenter_view),
    # Billing
    # billing.invoices_view),
    path("billing/invoices/", dashboard.coming_soon_view),
    # INVENTIONS
    path("inventions/disclosures/", inventions.invention_disclosures_view, name="inventions"),
    path("inventions/disclosures/file-upload/",
         files.upload_file),  # file.upload),
    # MODULES
    path("modules/families/list/", modules.families_list_view),
    path("modules/families/add/", modules.families_create_view),
    path("modules/families-patent/add/", modules.families_create_patent_view),
    path("modules/families-design/add/", modules.families_create_design_view),
    path("modules/families-trademark/add/", modules.families_create_trademark_view),
    path("modules/families/detail/<int:pk>/", modules.families_detail_view),
    path("modules/families/edit/<int:pk>/", modules.families_update_view),
    path("modules/families/delete/<int:pk>/", modules.families_delete_view),

    path("modules/patents/list/", modules.patents_list_view),
    path("modules/patents/add/", modules.patents_create_view),
    path("modules/patents/adds/", modules.patents_create_views),
    path("modules/patents/detail/<int:pk>/", modules.patents_detail_view),
    path("modules/patents/edit/<int:pk>/", modules.patents_update_view),
    path("modules/patents/delete/<int:pk>/", modules.patents_delete_view),
    path('modules/inventor-autocomplete/', modules.inventor_autocomplete, name='inventor_autocomplete'),
    path('modules/applicant-autocomplete/', modules.applicant_autocomplete, name='applicant_autocomplete'),
    path("modules/patents/patent_pct_form_view/", modules.patent_pct_form_view, name='patent_pct_form_view'),
    path('app/modules/patents/add/<str:selected_countries>/', modules.patents_create_view,
         name='add_family_patent_with_countries'),

    path("modules/designs/list/", modules.designs_list_view),
    path("modules/designs/add/", modules.designs_create_view),
    path("modules/designs/detail/<int:pk>/", modules.designs_detail_view),
    path("modules/designs/edit/<int:pk>/", modules.designs_update_view),
    path("modules/designs/delete/<int:pk>/", modules.designs_delete_view),

    path("home/list/", modules.intellectual_property_view),
    path("home/lists/", dashboard.home_search_view),

    path("modules/trademarks/list/", modules.trademarks_list_view),
    path("modules/trademarks/add/", modules.trademarks_create_view),
    path("modules/trademarks/detail/<int:pk>/", modules.trademarks_detail_view),
    path("modules/trademarks/edit/<int:pk>/", modules.trademarks_update_view),
    path("modules/trademarks/delete/<int:pk>/", modules.trademarks_delete_view),
    # SETTINGS
    path("settings/", dashboard.coming_soon_view),
    # REPORTS
    path("reports/", dashboard.coming_soon_view),

    #related cases links
    path("modules/related_cases_view", modules.related_cases_view)
]
