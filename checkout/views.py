import json
import uuid
from datetime import date, timedelta

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

import stripe

from bag.contexts import bag_contents
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass
from profiles.models import UserProfile
from profiles.forms import UserProfileForm, UserForm
from .forms import OrderForm
from .models import OrderLineItem, Order


@require_POST
def cache_checkout_data(request):
    """ View to temp save checkout data """
    try:
        #  check if the order includes a class access package
        package_data = {}
        classes_data = []
        current_bag = bag_contents(request)
        package = current_bag['bag_items']['class_access_package']
        # store exercise class id numbers in meta data
        if len(current_bag['bag_items']['single_classes']) > 0:
            for item in current_bag['bag_items']['single_classes']:
                classes_data.append(item.id)
        # store package data in meta data
        if package:  # add required data to dict
            package_data['name'] = package.friendly_name
            package_data['type'] = package.type
            package_data['amount_of_tokens'] = package.amount_of_tokens
            package_data['expiry_date'] = (date.today() + timedelta(days=package.duration)).strftime("%d,%m,%Y")
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
            'has_account': request.user.is_authenticated,
            'package_data': json.dumps(package_data),
            'classes_data': json.dumps(classes_data),
        })
        return HttpResponse(status=200)
    except Exception as err:
        messages.error(request, f"Sorry, your payment can't be processed \
            right now. Please try again later. {err}")
        return HttpResponse(content=err, status=400)

def checkout(request):
    """ A view to render the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get('bag', {})

        form_data = {  # gather data from POST method
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():  # save order_form if valid
            order = order_form.save(commit=False)

            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            if bag['class_access_package']:
                try:
                    package = ClassAccessPackage.objects.get(id=bag['class_access_package'])
                    order_line_item = OrderLineItem(
                            order=order,
                            access_package=package,
                        )
                    order_line_item.save()
                except package.DoesNotExist:
                    messages.error(request, (
                        "The Class Access Package in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            for item_id in bag['single_classes']:
                try:
                    exercise_class = SingleExerciseClass.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                            order=order,
                            exercise_class=exercise_class,
                        )
                    order_line_item.save()
                except exercise_class.DoesNotExist:
                    messages.error(request, (
                        "One of the Exercise Classes in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "You can't checkout as there is nothing in your shopping bag")
            return redirect(reverse('view_bag'))

        if not request.user.is_authenticated and bag["class_access_package"]:
            messages.error(request, "You can't purchase a Class Access Package\
                 or Class Tokens without being signed in. Please sign in or\
                 create and account.")
            return redirect(reverse('account_login'))

        current_bag = bag_contents(request)
        grand_total = current_bag['total']
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )
        # check if user is authenticated to auto fill order form
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, "Stripe Public Key is missing. Please set it \
            and try again")

    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle sucessful checkouts"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        user_profile_object = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
            }
            # split full name into first and last
            list_name = order.full_name.split()
            user_data = {
                'first_name': list_name[0],
                'last_name': list_name[-1],
                'email': order.email,
                'username': user_profile_object.username,
            }

            user_profile_form = UserProfileForm(profile_data, instance=profile)
            user_form = UserForm(user_data, instance=user_profile_object)

            if user_profile_form.is_valid() and user_form.is_valid():
                try:
                    user_profile_form.save()
                    user_form.save()
                    messages.success(request, "Submitted Information Saved to Profile")
                except Exception as err:
                    messages.error(request, f"User Data Not Saved. Error message: {err}")
        else:
            messages.error(request, "User Data Not Saved")

    messages.success(request, f"Order sucessfully processed! {chr(10)}\
        Your order number is {order_number}.{chr(10)}A confirmation email will be sent \
            to {order.email}.")

    current_bag = bag_contents(request)
    # Save Class Access Package to Profile
    if current_bag['bag_items']['class_access_package']:
        package = current_bag['bag_items']['class_access_package']
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            profile.active_class_package = True
            profile.package_name = package.friendly_name
            profile.class_package_type = package.type
            if package.type == "TK":
                if not profile.class_tokens:  # if no tokens in account
                    profile.class_tokens = package.amount_of_tokens
                else:  # add tokens to current total
                    profile.class_tokens += package.amount_of_tokens
            profile.package_expiry = date.today() + timedelta(
                                      package.duration)
            profile.save()
    # Save Classes to Profile
    if len(current_bag['bag_items']['single_classes']) > 0:
        for item in current_bag['bag_items']['single_classes']:
            if request.user.is_authenticated:
                item.participants.add(user_profile_object)
                # add class to profile
                profile.classes.add(item)
                profile.save()
            else:
                # fill user data and add user to class list
                list_name = order.full_name.split()
                user_data = {
                    'first_name': list_name[0],
                    'last_name': list_name[-1],
                    'email': order.email,
                    'username': 'Guest_' + str(uuid.uuid4()),
                }
                user_form = UserForm(user_data)

                if user_form.is_valid():
                    try:
                        guest_user = user_form.save()
                        item.participants.add(guest_user)
                        messages.success(request, "Saved Guest info to Class")
                    except Exception as err:
                        messages.error(request, f"Guest Info Not Saved. Error message: {err}")
            item.remaining_spaces -= 1
            item.save()

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
