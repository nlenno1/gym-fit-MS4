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


def view_all_single_classes(request):
    """ A view to return all the single exercise classes"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()

    context = {
        'classes': classes,
        'class_categories': categories,
    }

    return render(request, 'classes/class_booking.html', context)


def filter_single_classes(request, category_id):
    """ A view to return all the single exercise classes"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()
    filtered_classes = []

    print("Category Selected : " + category_id)
    for item in classes:
        print(item.category.id)
        if str(item.category.id) == str(category_id):
            filtered_classes.append(item)

    context = {
        'classes': filtered_classes,
        'class_categories': categories,
    }

    return render(request, 'classes/class_booking.html', context)
