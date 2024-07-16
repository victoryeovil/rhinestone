from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from app.models import Inventor, Applicant, Licensor, Licensee, Consultant, Attorney
from app.forms import AttorneyForm, InventorForm, ApplicantForm, LicensorForm, LicenseeForm, ConsultantForm


def contact_detail_view(request, model_name, pk):
    model_name = model_name.capitalize()
    model = globals().get(model_name)
    if not model:
        return HttpResponse("Model not found", status=404)

    instance = get_object_or_404(model, pk=pk)
    form_class = globals().get(f'{model_name}Form')
    if not form_class:
        return HttpResponse("Form class not found", status=404)

    form = form_class(instance=instance)
    context = {'form': form, 'model_name': model_name, 'instance': instance}
    return render(request, 'app/address-book/contact_detail.html', context)


def contact_edit_view(request, model_name, pk):
    model_name = model_name.capitalize()
    model = globals().get(model_name)
    form_class = globals().get(f'{model_name}Form')

    if model is None or form_class is None:
        return HttpResponseNotFound("Model or Form not found")

    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    else:
        form = form_class(instance=instance)

    context = {'form': form, 'model_name': model_name, 'instance': instance}
    return render(request, 'app/address-book/contact_form.html', context)


def contact_delete_view(request, model_name, pk):
    model_name = model_name.capitalize()
    model = globals()[model_name]
    instance = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect('contacts')
    context = {'instance': instance, 'model_name': model_name}
    return render(request, 'app/address-book/contact_confirm_delete.html', context)
