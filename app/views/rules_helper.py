import datetime
from django.utils import timezone

from app.models.rules import AnnuityRules, CountryRules

def calculate_due_date(base_date, offset_days):
    return base_date + datetime.timedelta(days=offset_days)

def apply_general_rules(country, base_date_type, base_date):
    rules = CountryRules.objects.filter(country=country, base_date_type=base_date_type)
    today = timezone.now().date()
    due_dates = []

    for rule in rules:
        due_date = calculate_due_date(base_date, rule.offset_days)
        if due_date <= today:
            print(f"Action {rule.code} is due or past due! Description: {rule.description}")
        due_dates.append((rule.code, due_date))
    return due_dates

def apply_annuity_rules(country, pct_date):
    rules = AnnuityRules.objects.get(country=country)
    today = timezone.now().date()
    due_dates = []

    # Calculate initial annuity due date
    initial_due_date = calculate_due_date(pct_date, int(rules.initial_interval_years * 365))
    due_dates.append((1, initial_due_date))

    # Calculate subsequent annuities
    current_due_date = initial_due_date
    for year in range(2, 21):  # Calculate for 20 years as an example
        current_due_date = calculate_due_date(current_due_date, int(rules.subsequent_interval_years * 365))
        due_dates.append((year, current_due_date))

    return due_dates
