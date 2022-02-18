from django.shortcuts import render
from .models import ClassCategory, SingleExerciseClass

def view_class_categories(request):
    """ A view to return all the categories"""

    categories = ClassCategory.objects.all()

    context = {
        'class_categories': categories
    }

    return render(request, 'classes/our_classes.html', context)


def view_all_single_classes(request):
    """ A view to return all the single exercise classes"""

    classes = SingleExerciseClass.objects.all()
    categories = ClassCategory.objects.all()

    context = {
        'classes': classes,
        'class_categories': categories
    }

    return render(request, 'classes/class_booking.html', context)
