
from django.urls import path
from home import views
from django.contrib.auth import views as auth_views

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

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
]