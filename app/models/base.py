from typing import Iterable, Optional
from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True
    
    @property
    def meta(self):
        return self._meta
    
    @classmethod
    def get_field_names(cls, model: models.Model):
        return [f.name for f in model._meta.fields]
    
    @property
    def field_names(self):
        return self.get_field_names(self)
    
    @property
    def model_abbreviation(self):
        return "".join([sub[0] for sub in self._meta.verbose_name.split(" ")]).upper()
    
    def __str__(self) -> str:
        return self.model_abbreviation + "-" + f"{self.id}".rjust(8, "0")