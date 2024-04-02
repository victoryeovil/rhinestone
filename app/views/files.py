from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms.files import (
    FileForm
)
from app.models.files import (
    File
)
from app.functions.handle_uploaded_file import (
    handle_uploaded_file
)

from django.contrib import messages

def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        files = request.FILES.getlist("field")
        if form.is_valid():
            save_files = []
            for file in files:
                save_files.append(
                    File(
                        field="files/" + file.name,
                        model="test model",
                        instance_id=1
                    )
                )
                handle_uploaded_file(file)
            File.objects.bulk_create(save_files)
            messages.success(request, f"Item successfully created!")
    else:
        form = FileForm()
    return render(request, "app/files/file.html", {"form": form})
