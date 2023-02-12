from django import forms
from .models import Customer, Address
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Email address',
        'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'login-pwd'}))


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        min_length=5,
        max_length=40,
        help_text='Required')
    email = forms.EmailField(
        max_length=60,
        help_text='Required',
        error_messages={'required': 'Ups,you will need an email'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        v = Customer.objects.filter(username=username)
        if v.count():
            raise forms.ValidationError('Ups, this username already exists')
        return username

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Ups, passwords don't match")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Ups, this email is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'postcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-2 account-form', 'placeholder': 'Full Name'}
        )
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control mb-2 account-form',
                                                         'placeholder': 'Phone'})
        self.fields['address_line_1'].widget.attrs.update(
            {'class': 'form-control mb-2 account-form', 'placeholder': 'Address'}
        )
        self.fields['address_line_2'].widget.attrs.update(
            {'class': 'form-control mb-2 account-form', 'placeholder': 'Address'}
        )
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control mb-2 account-form', 'placeholder': 'City'}
        )
        self.fields['postcode'].widget.attrs.update(
            {'class': 'form-control mb-2 account-form', 'placeholder': 'Postcode'}
        )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Ups, we can't find that email address")
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email can't be changed",
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    username = forms.CharField(
        label='Username',
        min_length=5,
        max_length=40,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname',
                   'readonly': 'readonly'}))
    first_name = forms.CharField(
        label='Name',
        min_length=5,
        max_length=40,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = Customer
        fields = ('email', 'username', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
