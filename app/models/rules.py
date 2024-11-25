from django.db import models

class CountryRules(models.Model):
    country = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField()
    base_date_type = models.CharField(max_length=50)  # e.g., 'priority', 'pct', 'filing'
    offset_days = models.IntegerField()

    def __str__(self):
        return f"{self.country} - {self.code}"

class AnnuityRules(models.Model):
    country = models.CharField(max_length=100)
    initial_interval_years = models.FloatField()
    subsequent_interval_years = models.FloatField()

    def __str__(self):
        return f"{self.country} Annuity Rules"
