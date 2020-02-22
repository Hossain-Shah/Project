from django.shortcuts import render,redirect
from .models import FileNumber, DocumentListing


def index(request):
    documentlists = DocumentListing.objects.all()
    files = FileNumber.objects.all()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            name_of_product = request.POST["Product description"]
            expires_on = str(request.POST["Date"])
            file_number = request.POST["File select"]
            content = name_of_product + " -- " + expires_on + " " + file_number
            Todo = DocumentListing(name_of_product=name_of_product, content=content, file_number=FileNumber.objects.get(file_number=file_number))
            Todo.save()
            return redirect("/")
        if "taskDelete" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for documentlist_id in checkedlist:
                documentlist = DocumentListing.objects.get(id=int(documentlist_id))
                documentlist.delete()
    return render(request, "index.html", {"documentlists": documentlists, "files":files})