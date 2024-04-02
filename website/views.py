# python libraries
import random

# 3rd party
from django.contrib.auth.models import make_password
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# import pdfkit

# import mine
from app import (
    models as app_models,
    forms as app_forms 
)

# Create your views here.
def index_view(request): return render(request, "website/index.html")

def contact_view(request): return render(request, "website/contact.html")

def gallery_view(request):
    return render(request, "website/gallery.html", {"gallery": []})

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    messages.info(request, f"Logged out successfully. See you soon!")
    return HttpResponseRedirect("/")


def login_view(request):
    if request.POST:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            messages.info(request, f"Login successful. Welcome!")
            next_view = request.GET.get("next") or "/app/"
            return HttpResponseRedirect(next_view)
        messages.error(request, f"Invalid credentials. Please try again!")
    return render(request, "website/login.html")


def register_view(request):
    form =  app_forms.RegisterForm()
    if request.POST:
        form =  app_forms.RegisterForm(data=request.POST)
        if form.is_valid():
            if app_models.User.objects.filter(username=form.cleaned_data.get("username")).exists():
                messages.error(request, "The username is taken!")
            else:
                user = app_models.Customer.objects.create(
                    username = form.cleaned_data.get("username"),
                    email = form.cleaned_data.get("email"),
                    password = make_password(form.cleaned_data.get("password")),
                    id_number = form.cleaned_data.get("username")
                )
                login(request, user)
                messages.info(request, f"Registration successful. Welcome {user}!")
                return HttpResponseRedirect("/app/")
        print("Errors", form.errors)
        print("Non Field Errors", form.non_field_errors())
    return render(request, "website/register.html", {"form": form})

def recover_view(request):
    if request.method == "POST":
        try:
            user = app_models.User.objects.get(email=request.POST.get("email"))
            new_password = random.choices(
                [chr(i) for i in (list(range(97, 123)) + list(range(65,91)) + list(range(48, 58)))],
                k=8
            )
            try:
                send_mail(
                    f"GFMP password reset",
                    "Dear {user}, your password has been changed to: \t {new_password} \t.Thank you!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                user.set_password(new_password)
                messages.info(request, f"Dear {user}, your password has been changed please check your email {user.email} and come back!")
            except:
                messages.error(request, "Password changed email failed to send! Try contacting us!")
        except:
            messages.error(request, "Unidentified email address!")
    return render(request, "website/recover.html")

