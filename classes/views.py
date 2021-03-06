from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile
from reviews.models import ClassCategoryReview
from products.constants import PACKAGE_TYPES
from .models import ClassCategory, SingleExerciseClass
from .forms import ClassCategoryForm, SingleExerciseClassForm

from .utils import (send_class_cancellation_email, send_update_email,
                    convert_ability_level_to_str)

# Class Categories


def view_class_categories(request):
    """A view to return all the categories"""

    categories = ClassCategory.objects.all().order_by("friendly_name")
    fav_categories = []
    # generate average rating
    for category in categories:
        (
            category.average_rating,
            category.numb_of_reviews,
        ) = category.generate_average_rating()
    # store favoutire categeory ids
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        for category in profile.fav_class_categories.all():
            fav_categories.append(category.id)

    context = {
        "class_categories": categories,
        "fav_categories": fav_categories,
    }

    return render(request, "classes/our_classes.html", context)


def view_single_class_category(request, category_id):
    """A view to return details about an individual class category"""
    # find category and generate average rating
    category = get_object_or_404(ClassCategory, pk=category_id)
    (
        category.average_rating,
        category.numb_of_reviews,
    ) = category.generate_average_rating()
    # find reviews for the category and order by date
    # create on newest to oldest
    reviews = ClassCategoryReview.objects.filter(
        review_subject=category
    ).order_by("-created_on")
    # find if user has a previous review
    previous_review = None
    if request.user.is_authenticated:
        previous_review = ClassCategoryReview.objects.filter(
            author=request.user, review_subject=category
        ).exists()
    # set favourite category variable for heart icon display
    fav_category = False
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if profile.fav_class_categories.filter(pk=category.id).exists():
            fav_category = True

    context = {
        "category": category,
        "fav_category": fav_category,
        "reviews": reviews,
        "previous_review": previous_review,
    }

    return render(request, "classes/class_category_details.html", context)


def filter_classes_by_category(category_filter, classes):
    """Function to filter a selection of classes a category"""
    category_filter = ClassCategory.objects.get(pk=category_filter)
    filtered_classes = classes.filter(category=category_filter)
    category_filter_name = category_filter.friendly_name
    return category_filter_name, filtered_classes


def filter_classes_by_fav_category(request, classes):
    """Function to filter a selection of classes using
    favourite class categories list"""
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        profile.check_package_expired()
        category_ids = [item.id for item in profile.fav_class_categories.all()]
        filtered_classes = classes.all().filter(category__id__in=category_ids)
        filter_name = "Favourite Class Categories"
        return filter_name, filtered_classes


def classes_this_week(request):
    """A view to return all the single exercise classes in the current week"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()
    profile_tokens = None
    profile = None
    category_filter = ""
    filter_name = ""
    # generate the current date, list of dates for this week and a list of
    # classes that happen in the week that are properly formatted
    current_date = datetime.strptime(
        datetime.now().strftime("%Y,%m,%d"), "%Y,%m,%d"
    )
    this_week = [(current_date + timedelta(days=x)).strftime(
                 "%Y-%m-%d")for x in range(9)]
    selected_classes = classes.filter(
        class_date__gte=this_week[0], class_date__lt=this_week[-1]
    )

    if request.GET:
        category_filter = request.GET["category_filter"]
        # Check for all category option selected
        if category_filter == "all" or category_filter == "":
            filter_name = "all"
        elif category_filter == "fav_categories":
            filter_name, selected_classes = filter_classes_by_fav_category(
                request, selected_classes
            )
        else:  # Filter the classes by category
            filter_name, selected_classes = filter_classes_by_category(
                category_filter, selected_classes
            )

    # Check if classes displayed have happened yet
    now = datetime.now()
    for item in selected_classes:
        if item.class_date.strftime("%d:%m:%Y - ") + item.start_time.strftime(
            "%H:%M"
        ) <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            item.closed = True

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        profile.check_package_expired()

        # check if class id is in profile classes
        for item in selected_classes:
            if profile.classes.filter(id=item.id).exists():
                item.unavailable = True

        profile_tokens = profile.class_tokens

    # Create a list of dates that contain classes with a friendly date
    # formatted to display
    days_with_classes = []
    search_storage = []
    for item in selected_classes:
        if item.class_date not in search_storage:
            search_storage.append(item.class_date)
            days_with_classes.append(
                {
                    "date": item.class_date,
                    "text_date": item.class_date.strftime("%A %d %b"),
                }
            )
    # sort function from Stack Overflow (see README credits for link)
    days_with_classes_sorted = sorted(
        days_with_classes, key=lambda d: d["date"]
    )

    # format ability level attributes for display
    for item in selected_classes:
        convert_ability_level_to_str(item)

    context = {
        "classes": selected_classes,
        "class_categories": categories,
        "days_with_classes": days_with_classes_sorted,
        "category_filter": filter_name,
        "profile_tokens": profile_tokens,
        "show_bag_on_success": True,
        'profile': profile,
    }

    return render(request, "classes/classes_this_week.html", context)


def filter_single_classes(request):
    """A view to return all the single exercise classes
    filtered by date and category"""

    filtered_classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()
    category_filter = "None"
    category_filter_name = ""
    date_filter = datetime.today().strftime("%Y-%m-%d")
    profile_tokens = None
    profile = None

    if request.GET:
        # Check for category & date filters and
        # assign previous if none
        if (
            request.GET["category_filter"] == "None"
            and request.GET["previous_category_filter"] == "None"
        ):
            category_filter = "all"
        elif (
            request.GET["category_filter"] == "None"
            and request.GET["previous_category_filter"] != "None"
        ):
            category_filter = request.GET["previous_category_filter"]
        else:
            category_filter = request.GET["category_filter"]

        date_filter = request.GET["date_filter"]

        # Check for all category option selected
        if category_filter == "all" or category_filter == "":
            category_filter = "all"
        elif category_filter == "fav_categories":
            (
                category_filter_name,
                filtered_classes,
            ) = filter_classes_by_fav_category(request, filtered_classes)
        else:  # Filter the classes by category
            (
                category_filter_name,
                filtered_classes,
            ) = filter_classes_by_category(category_filter, filtered_classes)

    # Filter the Classes by date and order by start time
    filtered_classes = filtered_classes.filter(
        class_date=date_filter
    ).order_by("start_time")
    # Check if classes displayed have happened yet
    now = datetime.now()
    for item in filtered_classes:
        if item.class_date.strftime("%d:%m:%Y - ") + item.start_time.strftime(
            "%H:%M"
        ) <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            item.closed = True

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        profile.check_package_expired()

        # check if class id is in profile classes
        for item in filtered_classes:
            if profile.classes.filter(id=item.id).exists():
                item.unavailable = True

        profile_tokens = profile.class_tokens

    # format ability level attributes for display
    for item in filtered_classes:
        convert_ability_level_to_str(item)

    context = {
        "classes": filtered_classes,
        "class_categories": categories,
        "category_filter": category_filter,
        "category_filter_name": category_filter_name,
        "date_filter": date_filter,
        "profile_tokens": profile_tokens,
        "show_bag_on_success": True,
        "profile": profile,
    }

    return render(request, "classes/classes_by_day.html", context)


# Token Functions


@login_required()
def book_with_package(request, class_id):
    """book class using user tokens"""

    redirect_url = request.POST.get("redirect_url")
    exercise_class = SingleExerciseClass.objects.get(pk=class_id)
    profile = UserProfile.objects.get(user=request.user)
    profile.check_package_expired()
    # check the user profile for class in classes field
    if profile.classes.filter(id=exercise_class.id).exists():
        messages.error(
            request,
            f"You have already booked onto \
                            {exercise_class.info()} \
                            so you can not add it to your bag",
        )
    # check if the class is fully booked
    elif exercise_class.remaining_spaces == 0:
        messages.error(
            request,
            "Sorry, we can't make this booking as this \
            class is fully booked",
        )
    # check if user has enough tokens
    elif (
        profile.class_package_type
        == "\
            TK"
        and profile.class_tokens < exercise_class.token_cost
    ):
        messages.error(
            request,
            "Sorry, we can't make this booking as you \
            don't have enough Class Tokens remaining",
        )
    else:
        # add profile to class and update
        exercise_class.participants.add(profile.user)
        exercise_class.remaining_spaces -= 1
        exercise_class.save()
        # add class to profile and deduct tokens if required
        profile.classes.add(exercise_class)
        if profile.class_package_type == "TK":
            profile.class_tokens -= exercise_class.token_cost
            messages.info(request, f"You have \
            {profile.class_tokens} Class Tokens remaining")
        profile.save()
        messages.success(
            request,
            f"You have booked onto the class \
            {exercise_class.info()}.",
        )
    try:
        return redirect(redirect_url)
    except Exception as err:
        messages.error(request, f"{err}")
        return redirect("classes_this_week")


@login_required
def cancel_class_booking(request, class_id):
    """Cancel class and refund tokens"""

    exercise_class = SingleExerciseClass.objects.get(pk=class_id)
    profile = UserProfile.objects.get(user=request.user)
    profile.check_package_expired()
    # update exercise class
    exercise_class.participants.remove(profile.user)
    exercise_class.remaining_spaces += 1
    exercise_class.save()
    # update profile
    profile.classes.remove(exercise_class)
    profile.save()

    messages.success(request, f"You have cancelled your booking on the class \
        {exercise_class}")
    # check if user qualifies for a refund
    if date.today() >= exercise_class.class_date - timedelta(days=1):
        messages.info(
            request,
            "You have cancelled this class booking \
            but have not been issued a refund due to notice given",
        )
    else:
        # create refund package and add tokens and expiry date
        # if user has no active package
        if (not profile.class_package_type and
                not profile.active_class_package):
            profile.active_class_package = True
            profile.class_package_type = "TK"
            profile.package_name = "Refund Package"
            profile.class_tokens = exercise_class.token_cost
            if profile.package_expiry < date.today() + timedelta(days=42):
                profile.package_expiry = date.today() + timedelta(days=42)
            messages.info(
                request,
                f"You have been refunded {exercise_class.token_cost} \
                Class Token/s to a new class access package assigned \
                to your profile (Valid until \
                {profile.package_expiry.strftime('%d %b')})",
            )
        # add refund tokens to existing package and update expiry date
        elif (profile.class_package_type == "TK" and
              profile.active_class_package):
            profile.class_tokens += exercise_class.token_cost
            profile.package_expiry = date.today() + timedelta(days=48)
            messages.info(
                request,
                f"You have been refunded {exercise_class.token_cost} \
                Class Token/s (Valid until \
                {profile.package_expiry.strftime('%d %b')})",
            )
            messages.info(
                request,
                f"You have {profile.class_tokens} \
                token/s remaining",
            )
    profile.save()
    return redirect(reverse("profile"))

# Single Exercise Class CRUD Operations


@login_required
def add_single_exercise_class(request):
    """A view to allow Admin to add new single exercise class"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = SingleExerciseClassForm(request.POST)
        if form.is_valid():
            # schedule weekly classes
            weekly_class = form.cleaned_data.get("weekly_class")
            weekly_classes_until = form.cleaned_data.get(
                "weekly_classes_until"
            )
            # create single class
            exercise_class = form.save(commit=False)
            exercise_class.end_time = (
                datetime.combine(date.today(), exercise_class.start_time)
                + timedelta(minutes=exercise_class.duration)
            ).time()
            exercise_class.remaining_spaces = exercise_class.max_capacity
            exercise_class.save()
            messages.success(
                request,
                f"Successfully Created An \
                             Exercise Class {exercise_class}",
            )
            if weekly_class:  # check if this is a weekly class
                # generate date of next class
                current_date = exercise_class.class_date + timedelta(days=7)
                # iterate until the date is higher than the date selected
                while current_date <= weekly_classes_until:
                    # add all values to new object
                    new_exercise_class = SingleExerciseClass()
                    new_exercise_class.category = exercise_class.category
                    new_exercise_class.class_date = current_date
                    new_exercise_class.start_time = exercise_class.start_time
                    new_exercise_class.end_time = exercise_class.end_time
                    new_exercise_class.duration = exercise_class.duration
                    new_exercise_class.location = exercise_class.location
                    new_exercise_class.instructor = exercise_class.instructor
                    new_exercise_class.price = exercise_class.price
                    new_exercise_class.token_cost = exercise_class.token_cost
                    new_exercise_class.max_capacity = (
                        exercise_class.max_capacity
                    )
                    new_exercise_class.remaining_spaces = (
                        exercise_class.remaining_spaces
                    )
                    new_exercise_class.ability_level = (
                        exercise_class.ability_level
                    )
                    new_exercise_class.additional_notes = (
                        exercise_class.additional_notes
                    )
                    new_exercise_class.save()  # save new class
                    messages.success(
                        request,
                        f"Successfully Created An \
                             Exercise Class {new_exercise_class}",
                    )
                    current_date += timedelta(days=7)
            return redirect(reverse("classes_this_week"))
        else:
            messages.error(
                request,
                "Failed to create the Exercise Class\
                           . Please ensure the form is valid",
            )
    else:
        form = SingleExerciseClassForm()

    context = {
        "form": form,
    }

    return render(request, "classes/add_single_exercise_class.html", context)


@login_required
def edit_single_exercise_class(request, class_id):
    """A view to allow Admin to edit a single exercise class"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    exercise_class = get_object_or_404(SingleExerciseClass, id=class_id)

    if request.method == "POST":
        form = SingleExerciseClassForm(
            request.POST, request.FILES, instance=exercise_class
        )
        if form.is_valid():
            # max capacity less than the amount of people signed up check
            if form.cleaned_data['max_capacity'] < len(
                    exercise_class.participants.all()):
                messages.error(request, "There are more people signed up to the class \
                    than the new max capacity allows")
                return redirect(reverse("classes_this_week"))
            else:  # send updates class email
                send_update_email(class_id, form, request)
                exercise_class = form.save(commit=False)
                # adjust the remaining spaces value
                exercise_class.remaining_spaces = (
                    exercise_class.max_capacity - len(
                        exercise_class.participants.all()))
                exercise_class.end_time = (  # generate the end time
                    datetime.combine(date.today(), exercise_class.start_time)
                    + timedelta(minutes=exercise_class.duration)
                ).time()
                exercise_class.save()
                messages.success(
                    request, "Successfully Updated Exercise Class")
                return redirect(reverse("classes_this_week"))
        else:
            messages.error(
                request,
                "Failed to update Class Category. \
                           Please ensure the form is valid",
            )
    else:
        form = SingleExerciseClassForm(instance=exercise_class)
    messages.info(
        request,
        f"You are now editing the Class of {exercise_class}",
    )

    context = {
        "form": form,
        "exercise_class": exercise_class,
    }

    return render(request, "classes/edit_single_exercise_class.html", context)


@login_required
def delete_single_exercise_class(request, class_id):
    """A view to allow Admin to delete a single exercise class"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    exercise_class = get_object_or_404(SingleExerciseClass, id=class_id)
    # refund customers tokens
    refund_total = 0  # total amount of tokens refunded
    class_name = exercise_class.info()
    for user_profile in exercise_class.participants.all():
        refunded = False
        # if user is not a guest
        if (len(str(user_profile.username)) < 11 or
                str(user_profile.username)[0:11] != "Guest_User_"):
            profile = UserProfile.objects.get(user=user_profile)
            # UU packages don't get refunded
            # if the user currently doesn't have a package
            if not profile.active_class_package:
                profile.active_class_package = True
                profile.class_package_type = "TK"
                profile.class_tokens = exercise_class.token_cost
                profile.package_name = "Refund Package"
                # 12 weeks to use the refund tokens
                profile.package_expiry = date.today() + timedelta(days=84)
                profile.save()
                refund_total += exercise_class.token_cost
                refunded = True
            # if the user is on a token package
            elif profile.class_tokens and profile.class_package_type != PACKAGE_TYPES['UNLIMITED']:
                profile.class_tokens += exercise_class.token_cost
                profile.save()
                refund_total += exercise_class.token_cost
                refunded = True
        # send email to all class participants
        send_class_cancellation_email(exercise_class, user_profile, refunded)
    exercise_class.delete()
    messages.success(request, f"Exercise Class {class_name} Cancelled")
    messages.info(request, f"Refunded a total of {refund_total} Token/s \
        to customers booked onto the class of {class_name}")
    return redirect(reverse("classes_this_week"))


# Class Category CRUD Operations


@login_required
def add_class_category(request):
    """A view to allow Admin to add new class category"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ClassCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            # edit form data for category
            category.name = category.friendly_name.lower().replace(" ", "-")
            category.friendly_name = category.friendly_name.title()
            category.save()
            messages.success(
                request,
                "Successfully Created A \
                             Class Category",
            )
            return redirect(reverse("view_single_class_category",
                            args=[category.id]))
        else:
            messages.error(
                request,
                "Failed to create the Class Category\
                           . Please ensure the form is valid",
            )
    else:
        form = ClassCategoryForm()

    context = {
        "form": form,
    }

    return render(request, "classes/add_class_category.html", context)


@login_required
def edit_class_category(request, category_id):
    """A view to allow Admin to edit a class category"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    category = get_object_or_404(ClassCategory, id=category_id)

    if request.method == "POST":
        form = ClassCategoryForm(
            request.POST, request.FILES, instance=category
        )
        if form.is_valid():
            category = form.save()
            # edit form data for category
            category.name = category.friendly_name.lower().replace(" ", "-")
            category.friendly_name = category.friendly_name.title()
            category.save()
            messages.success(request, "Successfully Updated Class Category")
            return redirect(
                reverse("view_single_class_category", args=[category.id])
            )
        else:
            messages.error(
                request,
                "Failed to update Class Category. \
                           Please ensure the form is valid",
            )
    else:
        form = ClassCategoryForm(instance=category)
        messages.info(
            request,
            f'You are now editing the Class Access Package \
                      called "{category.friendly_name}"',
        )

    context = {
        "form": form,
        "category": category,
    }

    return render(request, "classes/edit_class_category.html", context)


@login_required
def delete_class_category(request, category_id):
    """A view to allow Admin to delete a class category"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse("home"))

    category = get_object_or_404(ClassCategory, id=category_id)
    # delete the classes that use this category and have been scheduled
    # including sending cancellation emails and issuing refunds
    classes_to_remove = SingleExerciseClass.objects.filter(
        category=category.id)
    for class_event in classes_to_remove:
        delete_single_exercise_class(request, class_event.id)

    category.delete()
    messages.success(request, "Category deleted")
    return redirect(reverse("view_class_categories"))


# Favourite Class List Functions


@login_required
def add_category_to_favs(request, category_id):
    """A view to allow user to add a class category
    to their favourties list"""

    profile = get_object_or_404(UserProfile, user=request.user)
    category = get_object_or_404(ClassCategory, pk=category_id)

    profile.fav_class_categories.add(category)
    messages.success(
        request,
        f"You have ADDED {category.friendly_name} to \
        your Class Category Favourites list",
    )
    try:
        redirect_url = request.POST.get("redirect_url")
        return redirect(redirect_url)
    except TypeError as err:
        messages.info(
            request,
            f"Redirected to all class categories \
            due to {err}",
        )
        return redirect(reverse("view_class_categories"))


@login_required
def remove_category_from_favs(request, category_id):
    """A view to allow user to remove a class category
    from their favourties list"""

    redirect_url = request.POST.get("redirect_url")
    profile = get_object_or_404(UserProfile, user=request.user)
    category = profile.fav_class_categories.get(id=category_id)

    profile.fav_class_categories.remove(category)
    messages.success(
        request,
        f"You have REMOVED {category.friendly_name} from \
        your Class Category Favourites list",
    )
    try:
        redirect_url = request.POST.get("redirect_url")
        return redirect(redirect_url)
    except TypeError as err:
        messages.info(
            request,
            f"Redirected to all class categories \
            due to {err}",
        )
        return redirect(reverse("view_class_categories"))
