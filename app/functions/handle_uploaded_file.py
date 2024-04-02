from app.data.common import FILE_PATH
def handle_uploaded_file(f):
    with open(FILE_PATH + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)