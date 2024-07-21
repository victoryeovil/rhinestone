from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .fields import ImageField
from .base import BaseModel

from app import data
from app.functions.generate_id import generate_id


class Contact(BaseModel):
    MID = models.CharField("ID", max_length=10, unique=True, blank=True, null=True)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    address_line_1 = models.CharField(max_length=128, blank=True, null=True)
    address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    address_city = models.CharField(max_length=128, blank=True, null=True)
    address_state = models.CharField(max_length=128, blank=True, null=True)
    type = models.CharField(max_length=16, choices=[(i, i) for i in
                                                    ["Inventor", "Applicant", "Licensor", "Licensee", "Consultant",
                                                     "Associate", "Paralegal", "Attorney", "OtherProvider"]])

    def __str__(self):
        return f"{self.name} #{self.id}"

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        Contact.objects.filter(id=self.id).update(
            MID=generate_id(6, self.surname[:4], self.id))


class ContactDetailsMixin(models.Model):
    nationality = models.CharField(max_length=128, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country_of_registration = models.CharField(max_length=128, blank=True, null=True,
                                               choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        abstract = True


class Inventor(Contact, ContactDetailsMixin):
    inventor_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Inventor Number")
    title = models.CharField(max_length=12, choices=data.contact_titles.CONTACT_TITLES_CHOICES, null=True, blank=True)
    type_of_contract = models.CharField(max_length=12, choices=data.contracts.CONTRACT_TYPES_CHOICES, null=True,
                                        blank=True)
    employer_name = models.CharField(max_length=128, blank=True, null=True)
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True, verbose_name="Email")
    date_of_employment_termination = models.DateField(blank=True, null=True)
    commencement_date = models.DateField(blank=True, null=True, verbose_name="Date of Employment Commencement")
    address_line_3 = models.CharField(max_length=128, blank=True, null=True)  # New field for Address line 3
    county_state = models.CharField(max_length=128, blank=True, null=True,
                                    verbose_name="County/State",
                                    choices=data.countries.COUNTRIES_OPTIONS)  # New field for County/State
    profession = models.CharField(max_length=128, blank=True, null=True)  # New field for Profession
    is_applicant = models.BooleanField(default=False)  # New field to indicate if Inventor is also an Applicant

    def __str__(self):
        return self.inventor_no


class Applicant(Contact, ContactDetailsMixin):
    applicant_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Applicant Number")
    date_of_incorporation = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True, choices=[(i, i) for i in ["Active", "Deactive"]])
    is_inventor = models.BooleanField(default=False)  # New field to indicate if Applicant is also an Inventor

    def __str__(self):
        return self.name if self.name else "Unnamed Applicant"


class Licensor(Contact, ContactDetailsMixin):
    licensor_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Licensor Number")
    title = models.CharField(max_length=12, choices=data.contact_titles.CONTACT_TITLES_CHOICES, null=True, blank=True)
    type_of_contract = models.CharField(max_length=12, choices=data.contracts.CONTRACT_TYPES_CHOICES, null=True,
                                        blank=True)
    employer_name = models.CharField(max_length=128, blank=True, null=True)
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True, verbose_name="Email")
    date_of_contract = models.DateField(blank=True, null=True)
    date_of_employment_termination = models.DateField(blank=True, null=True)
    commencement_date = models.DateField(blank=True, null=True)
    contractor = models.CharField(max_length=128, blank=True, null=True)
    contractor_type = models.CharField(max_length=128, blank=True, null=True)
    employer_address_line_1 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_city = models.CharField(max_length=128, blank=True, null=True)
    employer_address_state = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.licensor_no if self.licensor_no else "Unnamed Licensor"


class Licensee(Contact, ContactDetailsMixin):
    licensee_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Licensee Number")
    date_of_incorporation = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.licensee_no if self.licensee_no else "Unnamed Licensee"


class Consultant(Contact, ContactDetailsMixin):
    consultant_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Consultant Number")

    def __str__(self):
        return self.consultant_no if self.consultant_no else "Unnamed Consultant"


class Associate(Contact, ContactDetailsMixin):
    Associate_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Associate Number")
    contact_person = models.CharField(max_length=128, blank=True, null=True, verbose_name="Contact Person")
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True, verbose_name="Email")
    office_contact = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True, verbose_name="Country",
                               choices=data.countries.COUNTRIES_OPTIONS)
    fax_number = models.CharField(max_length=128, blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.Associate_no if self.Associate_no else "Unnamed Associate"


class Paralegal(Contact, ContactDetailsMixin):
    paralegal_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Paralegal Number")

    def __str__(self):
        return self.paralegal_no if self.paralegal_no else "Unnamed Paralegal"


class Attorney(Contact, ContactDetailsMixin):
    attorney_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Attorney Number")

    def __str__(self):
        return self.attorney_no if self.attorney_no else "Unnamed Attorney"


class OtherProvider(Contact, ContactDetailsMixin):
    authorizer = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="other_authorizer", verbose_name="Authorizer")
    provider_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="Provider Number")
    applicants = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="other_applicant", verbose_name="Applicant")
    country = models.CharField(max_length=128, blank=True, null=True, verbose_name="Country", choices=data.countries.COUNTRIES_OPTIONS)
    address_line_3 = models.CharField(max_length=128, blank=True, null=True, verbose_name="Address Line 3")
    contact_person = models.CharField(max_length=128,verbose_name="Contact Person(s)")
    zip_code = models.CharField(max_length=250, blank=True, null=True, verbose_name="Postal/Zip Code")
    notes = models.TextField(max_length=512, blank=True, null=True)
    country_states = models.CharField(max_length=128, blank=True, null=True, verbose_name="County/State")

    def __str__(self):
        return self.applicants.name if self.applicants and self.applicants.name else "Unnamed Provider"


@receiver(post_save, sender=Contact)
def update_contact_mid(sender, instance, **kwargs):
    if not instance.MID:
        instance.MID = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Contact)
def update_otherprovider_mid(sender, instance, **kwargs):
    if not instance.MID:
        instance.MID = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Inventor)
def update_inventor_number(sender, instance, **kwargs):
    if not instance.inventor_no:
        instance.inventor_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Applicant)
def update_applicant_number(sender, instance, **kwargs):
    if not instance.applicant_no:
        instance.applicant_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Licensor)
def update_licensor_number(sender, instance, **kwargs):
    if not instance.licensor_no:
        instance.licensor_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Licensee)
def update_licensee_number(sender, instance, **kwargs):
    if not instance.licensee_no:
        instance.licensee_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Consultant)
def update_consultant_number(sender, instance, **kwargs):
    if not instance.consultant_no:
        instance.consultant_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Associate)
def update_Associate_number(sender, instance, **kwargs):
    if not instance.Associate_no:
        instance.Associate_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Paralegal)
def update_paralegal_number(sender, instance, **kwargs):
    if not instance.paralegal_no:
        instance.paralegal_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()


@receiver(post_save, sender=Attorney)
def update_attorney_number(sender, instance, **kwargs):
    if not instance.attorney_no:
        instance.attorney_no = generate_id(6, instance.surname[:4], instance.id)
        instance.save()
