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
    context = {"notebook":queryset}
    return render(request, "books.html", context)


# sare code ka meaning malum karna hai