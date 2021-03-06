from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import ClassAccessPackage
from products.constants import PACKAGE_TYPES
from classes.models import SingleExerciseClass
from profiles.models import UserProfile


def view_bag(request):
    """View to render the shopping bag"""

    return render(
        request,
        "bag/bag.html",
    )


@login_required
def add_package_to_bag(request, item_id):
    """View to add a package to the shopping bag"""

    package = get_object_or_404(ClassAccessPackage, pk=item_id)
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get(
        "bag", {"class_access_package": None, "single_classes": []}
    )

    profile = get_object_or_404(UserProfile, user=request.user)
    profile.check_package_expired()
    # check if user has an active unlimited use class access package
    if profile.active_class_package and (
            profile.class_package_type == PACKAGE_TYPES['UNLIMITED']):
        messages.error(
            request,
            f"You can not add {package.friendly_name} to your bag \
                       as you currently have an active Unlimited Use Package",
        )
        return redirect(redirect_url)
    # check if user has an active tokens package
    if profile.active_class_package and (
            profile.class_package_type == PACKAGE_TYPES['TOKENS']):
        messages.info(
            request,
            "Purchasing a new Token Package with tokens on \
                      your account will add the new tokens to your amount and \
                      update their expiry date",
        )
    # package replacement message
    if bag["class_access_package"] is not None:
        messages.warning(
            request,
            "The previously selected Class Access Package has been removed",
        )
    # add package to the bag
    bag["class_access_package"] = item_id
    messages.success(
        request, f"Added {package.friendly_name} to your shopping bag"
    )
    # store the bag in the session storage
    request.session["bag"] = bag

    return redirect(redirect_url)


def add_single_class_to_bag(request, item_id):
    """View to add a single class to the shopping bag"""

    exercise_class = get_object_or_404(SingleExerciseClass, pk=item_id)
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get(
        "bag", {"class_access_package": None, "single_classes": []}
    )

    if exercise_class:
        # check if user is in the class participants list
        if exercise_class.participants.filter(id=request.user.id):
            messages.error(
                request,
                f"You have already booked onto \
                           {exercise_class} so you can not add it to your bag",
            )
            return redirect(redirect_url)
        # check if class is fully booked
        elif exercise_class.remaining_spaces == 0:
            messages.error(
                request,
                "Sorry, we can't add this to your bag as this\
                class is fully booked",
            )
    # add to bag if it is not in the bag already
    if item_id not in bag["single_classes"]:
        bag["single_classes"].append(item_id)
        messages.success(request, f"Added {exercise_class} to your bag")
    else:
        messages.warning(request, f"{exercise_class} is already in your bag")

    request.session["bag"] = bag

    return redirect(redirect_url)


def remove_from_bag(request, product_type, item_id):
    """View to remove items from the bag"""

    try:
        bag = request.session.get(
            "bag", {"class_access_package": None, "single_classes": []}
        )
        # remove package from bag
        if product_type == "package":
            package = get_object_or_404(ClassAccessPackage, pk=item_id)
            bag["class_access_package"] = None
            messages.success(
                request, f"Removed {package.friendly_name} from your bag"
            )
        # remove class from bag
        elif product_type == "single_class":
            exercise_class = get_object_or_404(SingleExerciseClass, pk=item_id)
            bag["single_classes"].remove(item_id)
            messages.success(
                request,
                f"Removed {exercise_class} from your bag",
            )
        # store the bag in the session storage
        request.session["bag"] = bag
    except Exception as err:
        messages.error(request, f"Error removing item: {err}")

    return redirect(reverse("view_bag"))
