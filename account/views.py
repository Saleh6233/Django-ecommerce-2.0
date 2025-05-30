from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_active = False

            user.save()

            # Email verification setup (template)

            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')

    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')

    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                messages.success(request, 'You are now logged in')

                return redirect("dashboard")

    context = {'form': form}

    return render(request, 'account/my-login.html', context=context)


def user_logout(request):
    try:

        for key in list(request.session.keys()):

            if key == 'session_key':

                continue

            else:

                del request.session[key]

    except KeyError:

        pass

    messages.success(request, 'You have been logged out.')

    return redirect('store')


@login_required(login_url='my-login')
def dashboard(request):
    try:
        # Get the most recent order
        latest_order = Order.objects.filter(
            user=request.user).order_by('-date_ordered').first()

        order_data = None
        if latest_order:
            order_items = OrderItem.objects.filter(order=latest_order)
            order_data = {
                'order': latest_order,
                'order_items': order_items,
                'item_count': order_items.count(),
            }

    except Exception as e:
        order_data = None

    context = {'order_data': order_data}
    return render(request, 'account/dashboard.html', context=context)


@login_required(login_url='my-login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, 'Your account has been updated')

            return redirect('dashboard')

    context = {'user_form': user_form}

    return render(request, 'account/profile-management.html', context=context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()

        messages.error(request, 'Your account has been deleted.')

        return redirect('store')

    return render(request, 'account/delete-account.html')


# Shipping view
@login_required(login_url='my-login')
def manage_shipping(request):
    try:

        shipping_address = ShippingAddress.objects.get(user=request.user)

    except ShippingAddress.DoesNotExist:

        shipping_address = None

    form = ShippingForm(instance=shipping_address)

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping_address)

        if form.is_valid():
            shipping_user = form.save(commit=False)

            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_orders(request):
    try:
        # Fetch all orders associated with the current user
        orders = Order.objects.filter(user=request.user)

        # For each order, get its associated order items
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(
                order=order)  # Get all items for this order
            orders_with_items.append(
                {'order': order, 'order_items': order_items})

        # Pass the orders and their items to the context
        context = {'orders_with_items': orders_with_items}

        return render(request, 'account/track-orders.html', context=context)

    except Exception as e:
        # Optionally, you can log the exception to debug if needed
        return render(request, 'account/track-orders.html', {'error': str(e)})


@login_required(login_url='my-login')
def change_password(request):
    """
    View to allow a logged-in user to change their password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(
                request, 'Your password has been changed successfully. Please log in with your new password.')
            return redirect('my-login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'account/change-password.html', context=context)
