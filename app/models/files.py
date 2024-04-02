from django.db import models

from .base import BaseModel
from .fields import ImageField, FileField


class File(BaseModel):
    field = FileField(upload_to="files")
    model = models.CharField(max_length=64)
    instance_id = models.IntegerField()


class Image(File):
    img = ImageField(upload_to="files")
