from django.db import models

from .fields import ImageField
from .base import BaseModel

from app import data
from app.functions.generate_id import generate_id

class Contact(BaseModel):
    MID = models.CharField("ID", max_length=10, blank=True, null=True)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    address_line_1 = models.CharField(max_length=128, blank=True, null=True)
    address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    address_city = models.CharField(max_length=128, blank=True, null=True)
    address_state = models.CharField(max_length=128, blank=True, null=True)
    type = models.CharField(max_length=16, choices=[(i, i) for i in ["Inventor","Applicant","Licensor","Licensee","Consultant","Agent","Paralegal","Attorney"]])
    
    def __str__(self):
        return f"{self.name} #{self.id}"
    
    # def save(self, *args, **kwargs):
    #     if not self.MID:
    #         self.MID = self.id
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        Contact.objects.filter(id=self.id).update(
            MID=generate_id(6 , self.surname[0:4], self.id))


class Inventor(Contact):
    inventor_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="inventor number")
    title = models.CharField(max_length=12, choices=data.contact_titles.CONTACT_TITLES_CHOICES,null=True, blank=True)
    type_of_contract = models.CharField(max_length=12, choices=data.contracts.CONTRACT_TYPES_CHOICES)
    employer_name = models.CharField(max_length=10, blank=True, null=True)
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True,verbose_name="Email")
    date_of_contact = models.DateField(blank=True, null=True,verbose_name="Contract  Date")
    date_of_employment_termination = models.DateField(blank=True, null=True)
    commencement_date = models.DateField(blank=True, null=True)
    home = models.CharField(max_length=128, blank=True, null=True)
    contract = models.CharField(max_length=128, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    employer_nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    employer_address_line_1 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_city = models.CharField(max_length=128, blank=True, null=True)
    employer_address_state = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True, null=True)
    def __str__(self):
        return self.inventor_no

    def save(self, *args, **kwargs):
        super(Inventor, self).save(*args, **kwargs)
        Inventor.objects.filter(id=self.id).update(
            inventor_no=generate_id(6 , self.surname[0:4], self.id))

class Applicant(Contact):
    applicant_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="applicant_no")
    date_of_incorporation = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True, choices=[(i,i) for i in ["Active", "Deactive"]])
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country_of_registration = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.applicant_no

    def save(self, *args, **kwargs):
        super(Applicant, self).save(*args, **kwargs)
        Applicant.objects.filter(id=self.id).update(
            applicant_no=generate_id(6 , self.surname[0:4], self.id))

class Licensor(Contact):
    licensor_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="inventor number")
    title = models.CharField(max_length=12, choices=data.contact_titles.CONTACT_TITLES_CHOICES)
    type_of_contract = models.CharField(max_length=12, choices=data.contracts.CONTRACT_TYPES_CHOICES)
    employer_name = models.CharField(max_length=10, blank=True, null=True)
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True, verbose_name="Email")
    date_of_contract = models.DateField(blank=True, null=True)
    date_of_employment_termination = models.DateField(blank=True, null=True)
    commencement_date = models.DateField(blank=True, null=True)
    contractor = models.CharField(max_length=128, blank=True, null=True)
    contractor_type = models.CharField(max_length=128, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    employer_nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    employer_address_line_1 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_line_2 = models.CharField(max_length=128, blank=True, null=True)
    employer_address_city = models.CharField(max_length=128, blank=True, null=True)
    employer_address_state = models.CharField(max_length=128, blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.licensor_no

    def save(self, *args, **kwargs):
        super(Licensor, self).save(*args, **kwargs)
        Licensor.objects.filter(id=self.id).update(
            licensor_no=generate_id(6 , self.surname[0:4], self.id))
        
class Licensee(Contact):
    licensee_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="licensee_no")
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    date_of_incorporation = models.DateField(blank=True, null=True)
    country_of_registration = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.licensee_no

    def save(self, *args, **kwargs):
        super(Licensee, self).save(*args, **kwargs)
        Licensee.objects.filter(id=self.id).update(
            licensee_no=generate_id(6 , self.surname[0:4], self.id))

class Consultant(Contact):
    consultant_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="consultant_no")
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country_of_registration = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.consultant_no

    def save(self, *args, **kwargs):
        super(Consultant, self).save(*args, **kwargs)
        Consultant.objects.filter(id=self.id).update(
            consultant_no=generate_id(6 , self.surname[0:4], self.id))
        
class Agent(Contact):
    agent_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="agent_no")
    contact_person = models.CharField(max_length=10, blank=True, null=True,verbose_name="Contact")
    email_of_future_contact = models.EmailField(max_length=256, blank=True, null=True, verbose_name="Email")
    office_contact = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True, choices=[(i,i) for i in ["Active", "Deactive"]])
    fax_number = models.CharField(max_length=128, blank=True, null=True)
    contact_person = models.CharField(max_length=128, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    def __str__(self):
        return self.agent_no

    def save(self, *args, **kwargs):
        super(Agent, self).save(*args, **kwargs)
        Agent.objects.filter(id=self.id).update(
            agent_no=generate_id(6 , self.surname[0:4], self.id))

class Paralegal(Contact):
    paralegal_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="paralegal_no")
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country_of_registration = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.paralegal_no

    def save(self, *args, **kwargs):
        super(Paralegal, self).save(*args, **kwargs)
        Paralegal.objects.filter(id=self.id).update(
            paralegal_no=generate_id(6 , self.surname[0:4], self.id))

class Attorney(Contact):
    attorney_no = models.CharField(max_length=128, blank=True, null=True, verbose_name="applicant_no")
    nationality = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS)
    country_of_registration = models.CharField(max_length=10, blank=True, null=True, choices=data.countries.COUNTRIES_OPTIONS, verbose_name="Country")
    notes = models.TextField(max_length=512, blank=True, null=True)
    zip_postal_code = models.CharField("Zip/Postal Code", max_length=12, blank=True, null=True)
    def __str__(self):
        return self.attorney_no

    def save(self, *args, **kwargs):
        super(Attorney, self).save(*args, **kwargs)
        Attorney.objects.filter(id=self.id).update(
            attorney_no=generate_id(6 , self.surname[0:4], self.id))