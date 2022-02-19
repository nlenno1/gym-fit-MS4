from django.shortcuts import render
from .models import ClassAccessPackage

def view_class_access_packages(request):
    """ A view to return the class access packages available"""

    packages = ClassAccessPackage.objects.all()

    context = {
        'packages': packages
    }

    return render(request, 'products/join_us.html', context)
