from ctypes.wintypes import _FILETIME
from typing import Any, Dict, Optional, Union
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=64, required=True, initial="mike")
    email = forms.EmailField(initial="mzinyoni7@outlook.com")
    password = forms.CharField(widget=forms.PasswordInput(), initial="password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), initial="passwords")

    def clean(self) -> Optional[Dict[str, Any]]:
        super().clean()
        if self.cleaned_data.get("password") != self.cleaned_data.get("password_confirmation"):
            self.add_error(None, "Password confirmation failed!")
        return self.cleaned_data
