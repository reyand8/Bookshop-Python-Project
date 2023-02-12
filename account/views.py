from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth import login, logout

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .tokens import account_activation_token
from .models import Customer, Address
from orders.views import user_orders
from django.contrib import messages
from shop.models import Product
from orders.models import Order


@login_required
def get_wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    return render(request, 'account/account_orders/account_user_wishlist.html', {'wishlist': products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, product.title + ' has been removed from your WishList')
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, 'Added ' + product.title + ' to your WishList')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def registrate_account(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            user.email = registration_form.cleaned_data['email']
            user.set_password(registration_form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please, activate your account'
            message = render_to_string(
                'account/account_activation/account_activation.html',
                {'user': user,
                 'domain': current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
                 })
            user.email_user(subject=subject, message=message)
            return HttpResponse('The user was registered successfully. We sent you the activation email.')
    else:
        registration_form = RegistrationForm()
    return render(request, 'account/account_activation/registration.html', {'form': registration_form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/account_activation/account_activation_invalid.html')


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'account/account_orders/dashboard.html', {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/account_edit/account_edit.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


# Addresses

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, 'account/account_orders/account_user_addresses.html', {'addresses': addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        address_form = UserAddressForm()
    return render(request, 'account/account_edit/account_edit_addresses.html', {'form': address_form})


@login_required
def edit_address(request, id):
    if request.method == 'POST':
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'account/account_orders/account_edit_addresses.html', {'form': address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect('account:addresses')


@login_required
def set_default_address(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    previous_url = request.META.get('HTTP_REFERER')
    if 'delivery_address' in previous_url:
        return redirect('checkout:delivery_address')
    return redirect('account:addresses')


@login_required
def get_user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, 'account/account_orders/account_user_orders.html', {'orders': orders})
