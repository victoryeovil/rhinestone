from django.core.management.base import BaseCommand, CommandError
from app.models import (
    User
)
from app import (
    models as app_models,
    utilities as app_utils
)
from django.contrib.auth.models import Group, Permission
import random, datetime, pytz
from decimal import Decimal as D

random_names = [
    "Tanaka", "Charmaine", "Tafara", "Mitchie", "Mitchell", "Tadiwa", "John", "Ngonie", "Caleb", "Chichi", "Tinaye", "Josh",
    "Munashe", "Jones", "Mat", "Jeff", "Neuro", "Nelson", "Shinga", "Ray", "Sly", "Hawk", "Tim", "Tom", "David", "Nigga", "Coi",
    "Lisa", "Love", "Chommie"
]

placeholder = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Suscipit dicta quibusdam saepe voluptas molestiae, ipsam nesciunt praesentium modi aperiam voluptates qui molestias quaerat minima adipisci provident. Provident voluptatem perferendis quisquam!"
get_random_placeholder = lambda n: placeholder[:random.randint(0, n)]

def save_super_form(super_model, data):
    form_cls = app_utils.create_model_form(super_model)
    form =form_cls(data)
    try:
        assert form.is_valid()
    except AssertionError as e:
        print(super_model, form.errors)
        raise e
    return form.save()

class Command(BaseCommand):
    help = 'Quickly load dummy data.'

    def handle(self, *args, **options):
        try:
            app_models.Organization.objects.create()
            su = save_super_form(app_models.User, dict(
                username="su",
                is_staff=True,
                is_superuser=True,
                email="su@mail.com",
                first_name="Super",
                last_name="User",
                phone="+263000000000",
                password="password"
            ))
            for u in ["Kuda", "Mathew", "Munashe"]:
                save_super_form(app_models.User, dict(
                    username=u.lower(),
                    is_staff=True,
                    is_superuser=True,
                    email=f"{u.lower()}@mail.com",
                    first_name=u,
                    last_name=u,
                    phone="+263000000000",
                    password="password"
                ))
            
            for (i, e) in enumerate(["Chemhute Park", "Matidoda Park", "Rhinestone Inventions Disclosure Tools"]):
                sp = save_super_form(app_models.SuperProduct, dict(
                    name=e,
                    type="Burial Place"
                ))
                for (count, element) in [(0, "Single"), (1, "Double Unit"), (2, "Tripple Unit"), (3, "Family Close")]:
                    bp = save_super_form(app_models.BurialPlace, dict(
                        name=f"{e} {element}",
                        super_product=sp,
                        number_of_beneficiaries=count,
                        amount = i+1*D("500.00") + count*D("500.00")
                    ))
                    for i in range(3):
                        fname = random.choice(random_names)
                        lname = random.choice(random_names)
                        last_user = app_models.User.objects.last()
                        c = save_super_form(app_models.Customer, dict(
                            username=f"c{last_user.id}",
                            first_name=fname,
                            last_name=lname,
                            email=f"{fname[0]}{lname}_{last_user.id}@mail.com",
                            password="password",
                            phone="+263" + str(random.randint(1111111, 9999999)),
                            id_number=f"id#{last_user.id}",
                            created_by=su,
                        ))
                        bpp = save_super_form(app_models.BurialPlacePurchase, dict(
                                first_name = fname,
                                last_name = lname,
                                gender = random.choice(["M", "F"]),
                                DOB = datetime.date(1980, 2, 2),
                                phone = "+26300000000",
                                email = f"{fname[0]}{lname}_{i}@mail.com",
                                nationality = random.choice(["Zimbabwean"]),
                                language = random.choice(["English", "Shona"]),
                                race = random.choice(["Black", "White", "Latin", "Asian", "Native", "Other"]),
                                religion = random.choice(["Christian", "ATR", "Islam", "Hindi", "Budhist", "Atheist", "Jew", "Other"]),
                                marital_status = random.choice(["Maried", "Single", "Divorced", "Widowed", "Engaged", "Partnered"]),
                                spouse = random.choice([f"{random.choice(random_names)} {lname}", ""]),
                                id_number = "00-000000-00",
                                physical_address = "Harare",
                                postal_address = "Harare",
                                employer = random.choice(["Gorvenment", "Self Employed", ""]),
                                occupation = random.choice(["Doctor", "Engineer", "Accountant", "Lawyer"]),
                                purchased_by = c,
                                # purchase details,
                                product = bp,
                                # official use,
                                application_accepted = True,
                                initial_installment = D("50.00"),
                                # payment_period = models.DateField(blank=True, null=True),
                                payment_period = random.choice(app_models.PAYMENT_PERIODS)[0],
                                plot_number = f"Plot: ###",
                                authorized_signatory = random.choice([su, None, None])
                        ))
                        if random.choice([True, True]):
                            invoice = app_models.Invoice.objects.filter(purchase=bpp).first()
                            save_super_form(app_models.Payment, dict(
                                title = f"Initail Payment",
                                invoice = invoice,
                                amount = invoice.amount,
                                verified_by = random.choice([su, None]),
                                method = random.choice(["cash", "bank"]),
                                reference_number = f"ref-#{invoice.id}",
                            ))
                        for i in range(bp.number_of_beneficiaries):
                            bnf = save_super_form(app_models.Beneficiary, dict(
                                full_name = f"{random.choice(random_names)} {lname}",
                                age = random.randint(1, 65),
                                id_number = f"###{i}",
                                relationship = random.choice(["Sibling", "friend", "spouse", "churchmate", "workmate", "other"]),
                                created_by = c,
                                burial_place_purchase = bpp,
                            ))
                        
        
        except Exception as e:
            raise e
            # raise CommandError(str(e))
        self.stdout.write(self.style.SUCCESS(f"Done with loaddata"))