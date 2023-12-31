from django.shortcuts import render , redirect
from .models import *


def notebook(request):
    if request.method == "POST":
        data = request.POST

        note_name = data.get("note_name")
        note_description = data.get("note_description")

        books.objects.create(
            note_name = note_name,
            note_description = note_description,
        )

        return redirect("notebook")

    queryset = books.objects.all()

    if request.GET.get("Search"):
         queryset = queryset.filter(note_name__icontains = request.GET.get("Search"))

    context = {"notebook":queryset}
    return render(request, "books.html", context)

def delete_note(request, id):
    queryset = books.objects.get(id=id)
    queryset.delete()
    return redirect("notebook")

def update_note(request, id):
    queryset = books.objects.get(id=id)
    if request.method == "POST":
        data = request.POST

        note_name = data.get("note_name")
        note_description = data.get("note_description")
        
        queryset.note_name = note_name
        queryset.note_description = note_description
        queryset.save()
        return redirect("notebook")

    context = {"notebook": queryset}
    return render(request, "update_books.html", context)




# sare code ka meaning malum karna hai