import os

from django.contrib.auth import authenticate
# from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound


# from django.contrib.auth.models import User


# Create your views here.


def index(request):
    return redirect("/login")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/pdf")
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect("/login")


def pdf(request):
    fs = FileSystemStorage()
    filename = "C:/Users/DELL/Desktop/Roshan's Work/Django/Userproject/A.pdf"
    if request.user.is_anonymous:
        return redirect("/login")
    elif fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="A.pdf"' # user will be prompted with the browser’s open/save file
            response[
                'Content-Disposition'
            ] = 'inline; filename="A.pdf"'  # User will be prompted display a PDF in the browser
            return response

    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
