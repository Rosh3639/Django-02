
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('email', views.userEmail, name="email user"),
    path('success', views.successEmail, name="success email"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error', views.error, name="error"),
    path('viewpdf', views.view_pdf, name="viewpdf"),
    path('pdf', views.pdf, name="PDF"),
]