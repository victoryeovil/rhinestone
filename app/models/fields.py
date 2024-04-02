from django.core.validators import FileExtensionValidator
from django.db.models.fields import files as file_fields
from django.db import models


class ImageFieldFile(file_fields.ImageFieldFile):
    def url(self) -> str:
        try:
            return super().url
        except:
            return self.field.default


class ImageField(models.ImageField):
    attr_class = ImageFieldFile


class FieldFile(file_fields.FieldFile):
    def url(self) -> str:
        try:
            return super().url
        except:
            return self.field.default


class FileField(models.FileField):
    attr_class = FieldFile

