from django.shortcuts import render
from .models import ClassCategory

def view_class_categories(request):
    """ A view to return all the categories"""

    categories = ClassCategory.objects.all()

    context = {
        'class_categories': categories
    }

    return render(request, 'classes/our_classes.html', context)
