from django.shortcuts import render , redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# before authenticated
def homepage(request):
    queryset = books.objects.all()

    if request.GET.get("Search"):
         queryset = queryset.filter(note_name__icontains = request.GET.get("Search"))

    context = {"notebook":queryset}
    return render(request, "notebook.html", context)

# after authenticated
@login_required(login_url="/login/")
def notebook(request):
    if request.method == "POST":
        data = request.POST

        note_name = data.get("note_name")
        note_description = data.get("note_description")

        books.objects.create(
            note_name = note_name,
            note_description = note_description,
            user=request.user # Set the user field to the current user
        )

        return redirect("notebook")

    queryset = books.objects.all()

    if request.GET.get("Search"):
         queryset = queryset.filter(note_name__icontains = request.GET.get("Search"))

    context = {"notebook":queryset}
    return render(request, "books.html", context)

# delete information
@login_required(login_url="/login/")
def delete_note(request, id):
    book = get_object_or_404(books, id=id)
    # Check if the current user is the author of the book
    if request.user != book.user:
        messages.error(request, "You do not have permission to delete this Poem.")
        return redirect("notebook")
    
    book.delete()
    messages.success(request, "Poem deleted successfully.")
    return redirect("notebook")

# update information
@login_required(login_url="/login/")
def update_note(request, id):
    book = get_object_or_404(books, id=id)

    # Check if the current user is the author of the book
    if request.user != book.user:
        messages.error(request, "You do not have permission to update this Poem.")
        return redirect("notebook")

    if request.method == "POST":
        data = request.POST

        note_name = data.get("note_name")
        note_description = data.get("note_description")

        book.note_name = note_name
        book.note_description = note_description
        book.save()

        messages.success(request, "Poem updated successfully.")
        return redirect("notebook")

    context = {"notebook": book}
    return render(request, "update_books.html", context)


# login information
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid Username")
            return redirect("login_page")
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.info(request, "Invalid Password")
            return redirect("login_page")
        else:
            login(request, user)
            return redirect("notebook")
        
    return render(request, "login.html")

# logout information
def logout_page(request):
    logout(request)
    return redirect("/")

# register information
def register_page(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username = username).exists():
            messages.info(request, "Username already taken")
            return redirect("register_page")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")

        return redirect("login_page")
    context = {'show_register': True}
    return render(request, "register.html",context)