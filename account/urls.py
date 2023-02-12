from django.contrib.auth import views as account_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import (PasswordResetConfirmForm, PasswordResetForm,
                    LoginForm)

app_name = 'account'

urlpatterns = [
    # Login and Registration
    path('login/', account_views.LoginView.as_view(
        template_name='account/account_activation/login.html',
        form_class=LoginForm),
        name='login'),
    path('logout/', account_views.LogoutView.as_view(
        next_page='/account/login/'),
        name='logout'),
    path('registration/', views.registrate_account, name='registration'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'),
    # Reset Password
    path('password_reset/', account_views.PasswordResetView.as_view(
        template_name='account/account_reset/account_reset_password_form.html',
        success_url='password_reset_email_confirm',
        email_template_name='account/account_reset_password_form.html',
        form_class=PasswordResetForm),
        name='reset_password'),
    path('password_reset_confirm/<uidb64>/<token>', account_views.PasswordResetConfirmView.as_view(
        template_name='account/account_reset/account_reset_password_conf.html',
        success_url='/account/password_reset_complete/',
        form_class=PasswordResetConfirmForm),
        name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name="account/account_reset/account_reset_password_status.html"),
        name='password_reset_done'),
    path('password_reset_complete/', TemplateView.as_view(
        template_name="account/account_reset/account_reset_password_status.html"),
        name='password_reset_complete'),
    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(
        template_name="account/account_delete/account_delete_conf.html"),
        name='delete_confirmation'),
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default_address, name="set_default"),
    path("user_orders/", views.get_user_orders, name="user_orders"),
    path("wishlist", views.get_wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
]
