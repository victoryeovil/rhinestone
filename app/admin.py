from django.contrib import admin

from app.models import *


for model in [
    Contact,
    Inventor,
    Applicant,
    Licensor,
    Licensee,
    Consultant,
    Agent,
    Paralegal,
    Attorney,
    File,
    User,
    Invoice,
    Trademark,
    Patent,
    Family,
    Design,
    Country
]:
    @admin.register(model)
    class ModelAdmin(admin.ModelAdmin):
        list_display = ("id", "__str__")

