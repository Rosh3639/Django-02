from home.models import Users
from django.contrib.auth import authenticate
# from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


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
        user = User.objects.filter(username=username).first()
        if user is None:
            messages.success(request, 'Username Not Found.')
            return redirect('/login')

        # if pwd is None:
        #     messages.success(request, 'Password Incorrect')
        #     return redirect('/login')

        users_obj = Users.objects.filter(user=user).first()
        if not users_obj.is_verified:
            messages.success(request, 'Profile is not verified please check your mail!')
            return redirect('/login')

        if authenticate(username=username, password=password):
            if user is not None:
                login(request, user)
                return redirect("/pdf")
            else:
                return render(request, 'login.html')
    return render(request, 'login.html')

    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect("/pdf")
    #     else:
    #         return render(request, 'login.html')
    #
    # return render(request, 'login.html')


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
    # logout(request)
    # return redirect("/login")


def send_mail_after_registration(email, auth_token):
    subject = 'Your account need to be verified'
    message = f"Hi paste your link to verify your account http://127.0.0.1:8000/verify/{auth_token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


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

def pdf(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render(request, 'view_pdf.html')
