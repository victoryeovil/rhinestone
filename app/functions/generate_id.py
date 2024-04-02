def generate_id(length,letters,id):
    zeros = (length - len(letters)) * "0"
    return '{letters}{zeros}{id}'.format(letters=letters,zeros=zeros, id=str(id))
