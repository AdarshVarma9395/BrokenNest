from django.shortcuts import render

def notebook(request):
    return render(request, "books.html")
