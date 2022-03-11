from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from checkout.models import Order
from .models import UserProfile
from contact.models import ContactMessage

from .forms import UserProfileForm, UserForm


def profile(request):
    """Display User Profile"""
    profile_object = get_object_or_404(UserProfile, user=request.user)
    profile_object.check_package_expired()
    user_object = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile_object)
        user_form = UserForm(request.POST, instance=user_object)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(
                request,
                "Update failed. Please ensure the form is \
                           valid",
            )
    else:
        form = UserProfileForm(instance=profile_object)

    user_form = UserForm(instance=user_object)
    orders = profile_object.orders.all().order_by("-order_date")

    upcoming_classes = []
    previous_classes = []
    if profile_object.classes.all().exists():
        for item in profile_object.classes.order_by("class_date"):
            if item.class_date < date.today():
                previous_classes.append(item)
            elif item.class_date == date.today() and item.start_time.strftime(
                "%H:%M:%S"
            ) < datetime.now().strftime("%H:%M:%S"):
                previous_classes.append(item)
            else:
                upcoming_classes.append(item)
        previous_classes = sorted(
            previous_classes,
            key=lambda x: (x.class_date, x.start_time),
            reverse=True,
        )

    admin_messages = None
    if request.user.is_superuser:
        admin_messages = ContactMessage.objects.all()
        for item in admin_messages:
            item.message_sent = item.message_sent.strftime("%d/%m/%Y %H:%M")

    template = "profiles/profile.html"
    context = {
        "form": form,
        "user_form": user_form,
        "orders": orders,
        "profile": profile_object,
        "upcoming_classes": upcoming_classes,
        "previous_classes": previous_classes,
        "fav_class_list": profile_object.fav_class_categories.all(),
        "admin_messages": admin_messages,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """Display Previous Orders"""
    # Find the order
    order = get_object_or_404(Order, order_number=order_number)
    # Message to tell user that this is a previous order
    messages.info(
        request,
        (
            f"This is a past confirmation for order number {order_number}. "
            "A confirmation email was sent on the order date."
        ),
    )
    # store required data and render
    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
    }

    return render(request, template, context)
