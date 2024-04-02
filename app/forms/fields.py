# from django.core.validators import FileExtensionValidator
# from django.db.formsfields import files as file_fields
# from django import forms


# class ImageFieldFile(file_fields.ImageFieldFile):
#     def url(self) -> str:
#         try:
#             return super().url
#         except:
#             return self.field.default


# class ImageField(forms.ImageField):
#     attr_class = ImageFieldFile


# class FieldFile(file_fields.FieldFile):
#     def url(self) -> str:
#         try:
#             return super().url
#         except:
#             return self.field.default


# class FileField(formsFileField):
#     attr_class = FieldFile

