import crispy_forms
from django.core.exceptions import ValidationError
from django.forms import forms

from home.models import Users
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()


def send_mail_after_registration(email, auth_token):
    subject = 'Your account need to be verified'
    message = (
        f"Hi please paste this link in your browser to verify your account https://ai-research-pdf.herokuapp.com/{auth_token}")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    msg = EmailMessage(subject, message, from_email, recipient_list)
    EmailThread(msg).start()


def index(request):
    # return render(request, 'index.html')
    return redirect("/login")


def view_pdf(request):
    return render(request, 'view_pdf.html')


def loginUser(request):
    '''
    Function to login the successful user. By taking its data using post and get.
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/pdf')
        elif user is None:
            messages.error(request, 'Incorrect Username or Password ')
            return redirect('/login')

        users_obj = Users.objects.filter(user=user).first()
        if not users_obj.is_verified:
            messages.success(request, 'Account is not verified please check your mail!')
            return redirect('/login')

        if authenticate(username=username, password=password):
            if user is not None:
                login(request, user)
                return redirect("/pdf")
            else:
                return render(request, 'login.html')
    return render(request, 'login.html')


def registerUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            users_obj = Users.objects.create(user=user_obj, auth_token=auth_token)
            users_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/email')
        except Exception as e:
            print(e)
    return render(request, 'register.html')


def successEmail(request):
    return render(request, 'success.html')


def userEmail(request):
    return render(request, 'email.html')


def verify(request, auth_token):
    try:
        user_obj = Users.objects.filter(auth_token=auth_token).first()
        if user_obj:
            if user_obj.is_verified:
                messages.success(request, 'Account already verified!')
                return redirect('/login')

            user_obj.is_verified = True
            user_obj.save()
            messages.success(request, 'Your account has been verified!')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)


def error(request):
    return render(request, 'error.html')


def pdf(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render(request, 'view_pdf.html')


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
            return
        return email


''''
This was another alternative to display pdf but it wasn't able applicable  mobile!!
'''
# def pdf(request):
#     fs = FileSystemStorage()
#     filename = "C:/Users/DELL/Desktop/Roshan's Work/Django/Userproject/A.pdf"
#     if request.user.is_anonymous:
#         return redirect("/login")
#     elif fs.exists(filename):
#         with fs.open(filename, 'rb') as pdf:
#             response = HttpResponse(pdf.read(), content_type='application/pdf')
#             # response['Content-Disposition'] = 'attachment; filename="A.pdf"' # user will be prompted with the browser’s open/save file(Download the pdf)
#             response[
#                 'Content-Disposition'
#             ] = 'inline; filename="A.pdf"'  # User will be prompted display a PDF in the browser
#             return response
#     else:
#         return HttpResponseNotFound('The requested pdf was not found in our server.')
