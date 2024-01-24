from django.shortcuts import render , redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime


# before-authenticated-page
def homepage(request):
    queryset = books.objects.all()

    if request.GET.get("Search"):
         queryset = queryset.filter(note_name__icontains = request.GET.get("Search"))

    context = {"notebook":queryset}
    return render(request, "notebook.html", context)

# after-authenticated-page
@login_required(login_url="/login/")
def notebook(request):
    if request.method == "POST":
        data = request.POST

        note_name = data.get("note_name")
        note_description = data.get("note_description")
        created_time = datetime.datetime.now()

        books.objects.create(
            note_name = note_name,
            note_description = note_description,
            user=request.user, # Set the user field to the current user
            created_time = created_time,
        )

        return redirect("notebook")

    queryset = books.objects.all()

    if request.GET.get("Search"):
         queryset = queryset.filter(note_name__icontains = request.GET.get("Search"))

    context = {"notebook":queryset}
    return render(request, "books.html", context)

# delete-page
@login_required(login_url="/login/")
def delete_note(request, id):
    queryset = books.objects.get(id=id)
    queryset.delete()
    return redirect("notebook")

# update-page
@login_required(login_url="/login/")
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


# login-page
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

# logout-page
def logout_page(request):
    logout(request)
    return redirect("/")

# register-page
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







