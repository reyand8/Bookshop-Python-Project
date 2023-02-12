from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db import models
import uuid


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_field):
        other_field.setdefault('is_staff', True)
        other_field.setdefault('is_superuser', True)
        other_field.setdefault('is_active', True)
        if other_field.get('is_staff') is not True:
            raise ValueError('Ups! Superuser must be assigned to staff=True.')
        if other_field.get('is_superuser') is not True:
            raise ValueError('Ups! Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, username, password, **other_field)

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('Ups! You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    # Main
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    # Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(subject, message, 'one@one.com', [self.email], fail_silently=False,)

    def __str__(self):
        return self.username


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), on_delete=models.CASCADE)
    full_name = models.CharField(_('Full Name'), max_length=150)
    phone_number = models.CharField(max_length=20)
    postcode = models.CharField(_('Postcode'), max_length=20)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"
