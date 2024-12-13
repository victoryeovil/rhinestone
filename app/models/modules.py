from django.db import models, transaction

from app.models.contacts import Applicant, Inventor

from .fields import ImageField, FileField
from .base import BaseModel
from app import data
from app.data.common import CASE_TYPE
from app.functions.generate_id import generate_id

CHOICES = [(i, i) for i in
           ["Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired",
            "Published", "Registered"]]


class ModuleBaseModel(BaseModel):
    _official_numbers_fields = []
    _titles_fields = []
    _associates_fields = []
    _associates_refs_fields = []

    _wildcard = models.TextField(null=True, blank=True)
    official_numbers = models.TextField(null=True, blank=True)
    _official_numbers = models.TextField(null=True, blank=True)
    titles = models.TextField(null=True, blank=True)
    _titles = models.TextField(null=True, blank=True)
    _associates = models.TextField(null=True, blank=True)
    _associates_refs = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def after_save(self, *args, **kwargs) -> None:
        self.refresh_from_db()
        self._meta.model.objects.filter(pk=self.pk).update(
            _wildcard=" ".join([str(getattr(self, field_name)) for field_name in self.field_names]),
            _official_numbers=" ".join(
                [str(getattr(self, field_name)) for field_name in self._official_numbers_fields]),
            _titles=" ".join([str(getattr(self, field_name)) for field_name in self._titles_fields]),
            _associates=" ".join([str(getattr(self, field_name)) for field_name in self._associates_fields]),
        )

class FamilyNumberCounter(models.Model):
    prefix = models.CharField(max_length=2, unique=True)  # e.g., 'TM', 'DE', 'PF'
    last_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prefix} - {self.last_number}"


class Family(ModuleBaseModel):
    _official_numbers_fields = ["family_no"]
    _titles_fields = ["internal_title", "formal_title"]
    _associates_fields = ["licensor"]
    _associate_refs_fields = []

    case_no = models.CharField(verbose_name="Case No", max_length=128, blank=True, null=True)
    family_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Family No")
    internal_title = models.CharField(max_length=128, verbose_name="Internal Title")
    next_annuity_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Next Annuity No")
    formal_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="Formal Title")
    country = models.CharField(max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS,
                               verbose_name="Country")
    status = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in [
        "Open", "Pending", "Filed", "Abandoned", "Sold", "Licensed", "On Hold", "Opposed", "Registered"]], verbose_name="Status")
    sub_status = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in [
        "Open", "Pending", "Filed", "Abandoned", "Sold", "Licensed", "On Hold", "Opposed"]], verbose_name="Sub Status")
    type_of_filing = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Trademark", "Design", "Patent"]], verbose_name="Type of Filing")
    sub_filing = models.CharField(max_length=128, blank=True, null=True, verbose_name="Sub Filing")
    primary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL,
                                         related_name="family_primary_attorney_set", blank=True, null=True,
                                         verbose_name="Primary Attorney")
    secondary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL,
                                           related_name="family_secondary_attorney_set", blank=True, null=True,
                                           verbose_name="Secondary Attorney")
    primary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL,
                                          related_name="family_primary_paralegal_set", blank=True, null=True,
                                          verbose_name="Primary Paralegal")
    secondary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL,
                                            related_name="family_secondary_paralegal_set", blank=True, null=True,
                                            verbose_name="Secondary Paralegal")
    inventor = models.ManyToManyField(Inventor, blank=True)
    applicant = models.ManyToManyField(Applicant, blank=True)
    licenced = models.CharField(max_length=4, blank=True, null=True, choices=[
        (i, i) for i in ["Yes", "No"]], verbose_name="Licensed")
    licensor = models.ForeignKey("app.Licensor", on_delete=models.SET_NULL,
                                 related_name="family_licensor_set", blank=True, null=True, verbose_name="Licensor")
    cost_centre = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Cost -1", "Cost -2"]], verbose_name="Cost Centre")
    cost_centre_code = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Applicant 1", "Applicant 2"]], verbose_name="Cost Centre Code")
    keywords = models.CharField(max_length=128, blank=True, null=True, verbose_name="Keywords")

    def __str__(self):
        return str(self.family_no)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Determine the prefix based on the type_of_filing
            if self.type_of_filing == 'Trademark':
                prefix = 'TM'
            elif self.type_of_filing == 'Design':
                prefix = 'DE'
            else:
                prefix = 'PF'

            # Get or create the counter for this prefix
            counter, created = FamilyNumberCounter.objects.get_or_create(prefix=prefix)

            # Increment the last number
            counter.last_number += 1
            counter.save()

            # Format the new family number with leading zeros
            new_family_no = f"{prefix}{str(counter.last_number).zfill(5)}"

            # Update the family_no field with the new number
            self.family_no = new_family_no

            super(Family, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Patent(ModuleBaseModel):
    _official_numbers_fields = ["case_no"]
    _titles_fields = ["internal_title", "formal_title"]
    _associates_fields = ["associate", "associate_2"]
    _associate_refs_fields = ["associate_ref", "associate_ref_2"]
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name="Case Ref/Docket No", related_name="patent_family_set")
    case_no = models.CharField(verbose_name="Case No", max_length=128, blank=True, null=True)
    official_number = models.CharField(max_length=12, verbose_name="Official Number", blank=True, null=True)

    country = models.CharField(max_length=128, blank=True, null=True, choices=data.countries.PCT_COUNTRIES_OPTIONS,
                               verbose_name="Country")
    internal_title = models.CharField(verbose_name="Internal Title", max_length=128, blank=True, null=True)
    formal_title = models.CharField(verbose_name="Formal Title", max_length=128, blank=True, null=True)
    type_of_filing = models.CharField(max_length=128, default="Patent", blank=True, null=True,
                                      verbose_name="Type of Filing")
    # status = models.CharField(max_length=128, blank=True, null=True,default=CHOICES[1][1], choices=CHOICES, verbose_name="Status" )
    status = models.CharField(max_length=128, blank=True, null=True, verbose_name="Status", default=CHOICES[0][0])
    filing_type = models.CharField(max_length=128, blank=True, null=True, verbose_name="Filing type", default="Patent")
    sub_filing_type = models.CharField(max_length=128, blank=True, null=True, verbose_name="Sub-Filing Type")
    sub_status = models.CharField(max_length=128, blank=True, null=True, choices=[(
        i, i) for i in ["Licensed In", "Licensed Out", "Opposition For", "Opposition Against"]],
                                  verbose_name="Sub-Status")
    primary_attorney = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, related_name="patent_primary_attorney_set", blank=True, null=True,
        verbose_name="Attorney 1")
    secondary_attorney = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, related_name="patent_secondary_attorney_set", blank=True, null=True,
        verbose_name="Attorney 2")
    primary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, related_name="patent_primary_set", blank=True, null=True,
        verbose_name="Paralegal 1")
    secondary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, related_name="patent_secondary_set", blank=True, null=True,
        verbose_name="Paralegal 2")
    inventor = models.ManyToManyField(Inventor)
    associate = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                              related_name="patent_associate_set", blank=True, null=True, verbose_name="Associate")
    associate_ref = models.ForeignKey("app.Associate", on_delete=models.SET_NULL, related_name="patent_associate_ref_set",
                                  blank=True, null=True, verbose_name="Associate Ref")
    associate_2 = models.ForeignKey("app.Associate", on_delete=models.SET_NULL, related_name="patent_associate_2_set", blank=True,
                                null=True, verbose_name="Associate 2")
    associate_ref_2 = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                    related_name="patent_associate_ref_2_set", blank=True, null=True,
                                    verbose_name="Associate Reference 2")

    associate_2_ref = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                    related_name="patent_associate_ref_2_sets", blank=True, null=True,
                                    verbose_name="Associate Ref 2")
    cost_centre = models.ForeignKey("app.CostCenter",max_length=128, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Cost Centre", related_name="cost_center")
    licence = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Yes", "No"]], verbose_name="Licence")
    cost_centre_code = models.ForeignKey('app.CostCenter',max_length=128, blank=True, null=True,on_delete=models.SET_NULL, verbose_name="Cost Centre Code")
    priority_provisional_application_no = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Priority/Provisional Application No")
    priority_provisional_date = models.DateField(
        max_length=128, blank=True, null=True, verbose_name="Priority/Provisional Date")
    next_annuity_due = models.CharField(max_length=128, blank=True, null=True, verbose_name="Next Annuity Due")
    PCT_application_no = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="PCT Application No")
    PCT_application_Date = models.DateField(blank=True, null=True, verbose_name="PCT Application Date")
    PCT_Country = models.ManyToManyField(Country)
    annuity_no = models.IntegerField(blank=True, null=True, choices=[
        (i, i) for i in range(1, 16)], verbose_name="Annuity No")
    application_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="National Application No")
    application_date = models.DateField(blank=True, null=True, verbose_name="National App Date")
    taxs_paid_by = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Contact 1", "Contact 2", "Contact 3"]], verbose_name="Taxes Paid By")
    publication_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Publication No")
    publication_date = models.DateField(blank=True, null=True, verbose_name="Publication Date")
    patent_term_no_of_days = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Patent Term No of Days")
    grant_number = models.CharField(max_length=128, blank=True, null=True, verbose_name="Grant Number")
    grant_date = models.DateField(blank=True, null=True, verbose_name="Grant Date")
    large_small_entity = models.CharField(
        max_length=128, blank=True, null=True, choices=[(i, i) for i in ["Large", "Small"]],
        verbose_name="Large/Small Entity")
    case_type = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in CASE_TYPE], verbose_name="Case Type")
    notes = models.CharField(max_length=300, verbose_name="Notes", blank=True, null=True)
    # Field to store the PCT application date
    PCT_application_Date = models.DateField(blank=True, null=True, verbose_name="PCT Application Date")
    # Field to store the annuity due dates
    annuity_due_dates = models.JSONField(blank=True, null=True, verbose_name="Annuity Due Dates")
    # Field to store the payment statuses
    payment_statuses = models.JSONField(blank=True, null=True, verbose_name="Payment Statuses")

    def __str__(self):
        return self.case_no if self.case_no else "Patent: {}".format(self.id)

    def save(self, *args, **kwargs):
        super(Patent, self).save(*args, **kwargs)
        Patent.objects.filter(id=self.id).update(
            case_no=generate_id(7, 'PF', self.id))
        self.after_save(*args, **kwargs)


class Design(ModuleBaseModel):
    _official_numbers_fields = ["case_no", "next_annuity_no", "design_priority_no", "design_application_no",
                                "registration_no"]
    _titles_fields = ["internal_title", "formal_title"]
    _associates_fields = ["associate", "associate_2", "licensor"]
    _associate_refs_fields = ["associate_ref", "associate_ref_2"]

    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name="Case Ref/Docket No", related_name="design_family_set")
    case_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Case No")
    country = models.CharField(max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS,
                               verbose_name="Country")
    internal_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="Internal Title")
    formal_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="Formal Title")
    type_of_filing = models.CharField(max_length=128, default="Design", blank=True, null=True,
                                      verbose_name="Type of Filing")
    status = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in [
        "Open", "Pending", "Filed", "Allowed", "Granted(Live)", "Abandoned", "Granted(DEA)", "Converted", "Expired",
        "Published", "Registered"]], verbose_name="Status")
    notes = models.CharField(max_length=300, blank=True,null=True, verbose_name="Notes")
    filing_type = models.CharField(max_length=128, blank=True, null=True, verbose_name="Filing type", default="Patent")
    sub_filing_type = models.CharField(max_length=128, blank=True, null=True,verbose_name="Sub Filing Type")
    sub_status = models.CharField(max_length=128, blank=True, null=True, choices=[(
        i, i) for i in ["Licensed In", "Licensed Out", "Opposition For", "Opposition Against"]],
                                  verbose_name="Sub Status")
    primary_attorney = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, related_name="design_primary_attorney_set", blank=True, null=True,
        verbose_name="Primary Attorney")
    secondary_attorney = models.ForeignKey(
        "app.Attorney", on_delete=models.SET_NULL, related_name="design_secondary_attorney_set", blank=True, null=True,
        verbose_name="Secondary Attorney")
    primary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, related_name="design_primary_set", blank=True, null=True,
        verbose_name="Primary Paralegal")
    secondary_paralegal = models.ForeignKey(
        "app.Paralegal", on_delete=models.SET_NULL, related_name="design_secondary_set", blank=True, null=True,
        verbose_name="Secondary Paralegal")
    associate = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                              related_name="design_associate_set", blank=True, null=True, verbose_name="Associate")
    associate_ref = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                  related_name="design_associate_ref_set", blank=True, null=True, verbose_name="Associate Ref")
    associate_2 = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                related_name="design_Associates_2_set", blank=True, null=True, verbose_name="Associate 2")
    associate_2_ref = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                    related_name="design_associate_2_ref_set", blank=True, null=True,
                                    verbose_name="Associate 2 Ref")
    cost_centre = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Cost 1", "Cost 2"]], verbose_name="Cost Centre")
    licence = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Yes", "No"]], verbose_name="Licence")
    licensor = models.ForeignKey("app.Licensor", on_delete=models.SET_NULL,
                                 related_name="design_licensor_set", blank=True, null=True, verbose_name="Licensor")
    no_of_drawings = models.IntegerField(blank=True, null=True, choices=[
        (i, i) for i in range(1, 11)], verbose_name="Number of Drawings")
    no_of_views = models.IntegerField(blank=True, null=True, choices=[
        (i, i) for i in range(1, 101)], verbose_name="Number of Views")
    cost_centre_code = models.CharField(max_length=128, blank=True, null=True, choices=[
        (i, i) for i in ["Applicant 1", "Applicant 2", "Applicant 3"]], verbose_name="Cost Centre Code")
    next_taxes_date = models.DateField(blank=True, null=True, verbose_name="Next Taxes Date")
    next_annuity_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Next Annuity No")
    taxes_paid_by = models.CharField(max_length=128, blank=True, null=True, verbose_name="Taxes Paid By")
    expired_date = models.DateField(blank=True, null=True, verbose_name="Expired Date")
    design_priority_no = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Design Priority No")
    country = models.CharField(
        max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    date = models.DateField(blank=True, null=True, verbose_name="Date")
    design_application_no = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Design Application No")
    country = models.CharField(
        max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    date = models.DateField(blank=True, null=True, verbose_name="Date")
    registration_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Registration No")
    country = models.CharField(
        max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    date = models.DateField(blank=True, null=True, verbose_name="Date")
    design_file = FileField(
        upload_to="designs", blank=True, null=True, verbose_name="Design File")

    def __str__(self):
        return self.case_no

    def save(self, *args, **kwargs):
        super(Design, self).save(*args, **kwargs)
        Design.objects.filter(id=self.id).update(
            case_no=generate_id(6, 'D', self.id))
        self.after_save(*args, **kwargs)


class Trademark(ModuleBaseModel):
    _official_numbers_fields = ["case_no", "trademark_priority_no", "trademark_application_no",
                                "trademark_registration_no"]
    _titles_fields = ["internal_title", "formal_title"]
    _associates_fields = ["associate"]
    _associate_refs_fields = ["associate_ref"]

    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name="Case Ref/Docket No", related_name="trademark_family_set")
    case_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Case No")
    country = models.CharField(
        max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    
    # New fields added
    trademark_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="Trademark Name")
    type_of_trademark = models.CharField(max_length=128, blank=True, null=True, choices=[
        ('Device marks', 'Device marks'),
        ('Service marks', 'Service marks'),
        ('Collective marks', 'Collective marks'),
        ('Certification marks', 'Certification marks'),
        ('Well-known marks', 'Well-known marks'),
        ('Unconventional trademarks', 'Unconventional trademarks'),
    ], verbose_name="Type of Trademark")

    picture_of_trademark = ImageField(
        upload_to="trademarks", blank=True, null=True, verbose_name="Picture of Trademark")
    
    primary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL,
                                         related_name="trademark_primary_attorney_set", blank=True, null=True,
                                         verbose_name="Primary Attorney")
    secondary_attorney = models.ForeignKey("app.Attorney", on_delete=models.SET_NULL,
                                           related_name="trademark_secondary_attorney_set", blank=True, null=True,
                                           verbose_name="Secondary Attorney")
    associate = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                              related_name="trademark_associate_set", blank=True, null=True, verbose_name="Associate")
    associate_ref = models.ForeignKey("app.Associate", on_delete=models.SET_NULL,
                                  related_name="trademark_associate_ref_set", blank=True, null=True,
                                  verbose_name="Associate Ref")
    primary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL,
                                          related_name="trademark_primary_paralegal_set", blank=True, null=True,
                                          verbose_name="Primary Paralegal")
    secondary_paralegal = models.ForeignKey("app.Paralegal", on_delete=models.SET_NULL,
                                            related_name="trademark_secondary_paralegal_set", blank=True, null=True,
                                            verbose_name="Secondary Paralegal")
    
    trademark_priority_no = models.CharField(max_length=128, blank=True, null=True,
                                             verbose_name="Trademark Priority No")
    date = models.DateField(verbose_name="Tax Date", blank=True, null=True)
    trademark_application_no = models.CharField(max_length=128, blank=True, null=True,
                                                verbose_name="Trademark Application No")
    applicaation_date = models.DateField("Application date", blank=True, null=True)
    trademark_registration_no = models.CharField(max_length=128, blank=True, null=True,
                                                 verbose_name="Trademark Registration No")
    registration_date = models.DateField(blank=True, null=True, verbose_name="Registration Date")
    next_tax_date = models.DateField(blank=True, null=True, verbose_name="Next Tax Date")
    taxes_paid_by = models.CharField(max_length=128, blank=True, null=True, verbose_name="Taxes Paid By")
    does_it_expire = models.CharField(max_length=4, blank=True, null=True, choices=[
        (i, i) for i in ["Yes", "No"]], verbose_name="Does It Expire")
    notes = models.CharField(max_length=300,blank=True, null=True, verbose_name="Notes")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Expiry Date")
    type_of_filing = models.CharField(max_length=128, default="Design", blank=True, null=True,
                                      verbose_name="Type of Filing")
    classes = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 46)], 
        blank=True, 
        null=True,
        verbose_name="Classes"
    )
    

    def __str__(self):
        return self.case_no

    def save(self, *args, **kwargs):
        super(Trademark, self).save(*args, **kwargs)
        Trademark.objects.filter(id=self.id).update(
            case_no=generate_id(7, 'TM', self.id))
        self.after_save(*args, **kwargs)
