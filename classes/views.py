from datetime import datetime, timedelta

from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile
from .models import ClassCategory, SingleExerciseClass
from .forms import ClassCategoryForm, SingleExerciseClassForm



def send_class_cancellation_email(class_id):
        """Send the user a class cancellation email"""
        exercise_class = SingleExerciseClass.objects.get(id=class_id)
        for person in exercise_class.attendees:
            user = User.objects.get(id=person.id)
            subject = render_to_string(
                'classes/cancellation_emails/confirmation_email_subject.txt',
                {'class': exercise_class})
            body = render_to_string(
                'classes/cancellation_emails/confirmation_email_body.txt',
                {'user': user, 'contact_email': settings.DEFAULT_FROM_EMAIL})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )     


def view_class_categories(request):
    """ A view to return all the categories"""

    categories = ClassCategory.objects.all()

    context = {
        'class_categories': categories
    }

    return render(request, 'classes/our_classes.html', context)


def view_single_class_category(request, category_id):
    """ A view to return details about an individual class category"""

    category = get_object_or_404(ClassCategory, pk=category_id)

    context = {
        'category': category
    }

    return render(request, 'classes/class_category_details.html', context)


def filter_classes_by_category(category_filter, classes):
    """ Function to filter a selection of classes a category"""
    category_filter = ClassCategory.objects.get(pk=category_filter)
    filtered_classes = classes.filter(category=category_filter)
    category_filter_name = category_filter.friendly_name
    return category_filter_name, filtered_classes

def classes_this_week(request):
    """ A view to return all the single exercise classes"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    profile.check_package_expired()

    category_filter = ''
    filter_name = ''
    # generate the current date, list of dates for this week and a list of
    # classes that happen in the week that are properly formatted
    current_date = datetime.strptime(
                    datetime.now().strftime("%Y,%m,%d"), "%Y,%m,%d")
    this_week = [(current_date + timedelta(days=x)).strftime(
                "%Y-%m-%d") for x in range(7)]
    selected_classes = classes.filter(date__gte=this_week[0], date__lt=this_week[-1])

    if request.GET:
        category_filter = request.GET['category_filter']
        # Check for all category option selected
        if category_filter == 'all' or category_filter == '':
            filter_name = 'all'
        else:  # Filter the classes by category
            filter_name, selected_classes = filter_classes_by_category(category_filter, selected_classes)

    # Check if classes displayed have happened yet
    now = datetime.now()
    for item in selected_classes:
        if item.date.strftime("%d:%m:%Y - ") + item.start_time.strftime("%H:%M") <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            item.closed = True

    # check if class id is in profile classes
    for item in selected_classes:
        if profile.classes.filter(id=item.id).exists():
            item.unavailable = True

    # Create a list of dates that contain classes with a friendly date
    # formatted to display
    days_with_classes = []
    search_storage = []
    for item in selected_classes:
        if item.date not in search_storage:
            search_storage.append(item.date)
            days_with_classes.append({
                'date': item.date,
                'text_date': item.date.strftime("%A %d %b"),
            })
    days_with_classes_sorted = sorted(days_with_classes, key=lambda d: d['date'])

    context = {
        'classes': selected_classes,
        'class_categories': categories,
        'days_with_classes': days_with_classes_sorted,
        'category_filter': filter_name,
    }

    return render(request, 'classes/classes_this_week.html', context)


def filter_single_classes(request):
    """ A view to return all the single exercise classes"""

    filtered_classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()
    category_filter = 'None'
    category_filter_name = ''
    date_filter = datetime.today().strftime('%Y-%m-%d')
    profile = UserProfile.objects.get(user=request.user)
    profile.check_package_expired()

    if request.GET:
        # Check if category or date filters are None and assign previous values if true
        if request.GET['category_filter'] != 'None':
            category_filter = request.GET['category_filter']
        else:
            category_filter = request.GET['previous_category_filter']

        date_filter = request.GET['date_filter']

        # Check for all category option selected
        if category_filter == 'all' or category_filter == '':
            category_filter = 'all'
        else:  # Filter the classes by category
            category_filter_name, filtered_classes = filter_classes_by_category(category_filter, filtered_classes)

    # Filter the Classes by date and order by start time
    filtered_classes = filtered_classes.filter(date=date_filter).order_by('start_time')
    # Check if classes displayed have happened yet
    now = datetime.now()
    for item in filtered_classes:
        if item.date.strftime("%d:%m:%Y - ") + item.start_time.strftime("%H:%M") <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            item.closed = True

    # check if class id is in profile classes
    for item in filtered_classes:
        if profile.classes.filter(id=item.id).exists():
            item.unavailable = True

    context = {
        'classes': filtered_classes,
        'class_categories': categories,
        'category_filter': category_filter,
        'category_filter_name': category_filter_name,
        'date_filter': date_filter,
    }

    return render(request, 'classes/classes_by_day.html', context)

# Single Exercise Class CRUD Operations


@login_required
def add_single_exercise_class(request):
    """ A view to allow Admin to add new single exercise class """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    if request.method == "POST":
        form = SingleExerciseClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created An \
                             Exercise Class")
            return redirect(reverse('add_single_exercise_class'))
        else:
            messages.error(request, "Failed to create the Exercise Class\
                           . Please ensure the form is valid")
    else:
        form = SingleExerciseClassForm()

    context = {
        'form': form,
    }

    return render(request, 'classes/add_single_exercise_class.html', context)


# Class Category CRUD Operations


@login_required
def add_class_category(request):
    """ A view to allow Admin to add new class category """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    if request.method == "POST":
        form = ClassCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created A \
                             Class Category")
            return redirect(reverse('view_class_categories'))
        else:
            messages.error(request, "Failed to create the Class Category\
                           . Please ensure the form is valid")
    else:
        form = ClassCategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'classes/add_class_category.html', context)
