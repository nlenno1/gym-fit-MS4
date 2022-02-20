from datetime import datetime, timedelta

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ClassCategory, SingleExerciseClass


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


def classes_this_week(request):
    """ A view to return all the single exercise classes"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()

    for item in classes:
        item.friendly_date = item.date.strftime("%d/%m/%Y")

    today = datetime.now()
    current_date = today.strftime("%Y,%m,%d")
    current_date_temp = datetime.strptime(current_date, "%Y,%m,%d")
    this_week = []
    for x in range(6):
        newdate = current_date_temp + timedelta(days=x)
        this_week.append(newdate)

    selected_classes = [item for item in classes if str(item.date) > str(this_week[0]) and str(item.date) < str(this_week[-1])]

    days_with_classes = []
    for item in selected_classes:
        if item.friendly_date not in days_with_classes:
            days_with_classes.append({
                'friendly_date': item.friendly_date,
                'text_date': item.date.strftime("%A %d %b"),
            })

    if request.GET:
        # Check if category or date filters are None and assign previous values if true
        if request.GET['category_filter'] == 'None':
            category_filter = request.GET['current_category_filter']
        else:
            category_filter = request.GET['category_filter']

        # Check for all category option selected
        if category_filter == 'all' or category_filter == '':
            selected_filter_name = 'all'
        else:  # Filter the classes by category
            selected_classes = [item for item in selected_classes if str(item.category.id) == str(category_filter)]
            selected_filter_name_list = [item.friendly_name for item in categories if str(item.id) == str(category_filter)]
            selected_filter_name = selected_filter_name_list[0]

    else:  # Set defaults and todays date to filter classes
        category_filter = ''
        selected_filter_name = ''

    context = {
        'classes': selected_classes,
        'class_categories': categories,

        'days_with_classes': days_with_classes,

        'selected_category_filter': selected_filter_name,
        'current_category_filter': category_filter,
    }

    return render(request, 'classes/classes_this_week.html', context)


def filter_single_classes(request):
    """ A view to return all the single exercise classes"""

    filtered_classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()

    if request.GET:
        print(request.GET)
        selected_filter_name_list = []

        # Check if category or date filters are None and assign previous values if true
        if request.GET['category_filter'] == 'None':
            category_filter = request.GET['current_category_filter']
        else:
            category_filter = request.GET['category_filter']

        date_filter = request.GET['date_filter']
        # Check for all category option selected
        if category_filter == 'all' or category_filter == '':
            selected_filter_name = 'all'
        else:  # Filter the classes by category
            filtered_classes = [item for item in filtered_classes if str(item.category.id) == str(category_filter)]
            selected_filter_name_list = [item.friendly_name for item in categories if str(item.id) == str(category_filter)]
            selected_filter_name = selected_filter_name_list[0]

    else:  # Set defaults and todays date to filter classes
        category_filter = ''
        selected_filter_name = ''
        date_filter = datetime.today().strftime('%Y-%m-%d')

    # Filter the Classes by day if a date is selected
    if date_filter != '':
        filtered_classes = [item for item in filtered_classes if str(item.date) == str(date_filter)]

    context = {
        'classes': filtered_classes,
        'class_categories': categories,

        'selected_category_filter': selected_filter_name,
        'current_category_filter': category_filter,

        'date_filter': date_filter,
    }

    return render(request, 'classes/classes_by_day.html', context)