from django.shortcuts import render
from .models import ClassAccessPackage

from datetime import date, timedelta

def view_class_access_packages(request):
    """ A view to return the class access packages available"""

    packages = ClassAccessPackage.objects.all()

    tokens = []
    unlimited = []

    for package in packages:
        if package.type == "UU":
            unlimited.append(package)
        else:
            tokens.append(package)

    for package in unlimited:
        package.today_expires = date.today() + timedelta(days=package.duration)

    context = {
        'token_packages': tokens,
        'unlimited_packages': unlimited,
    }

    return render(request, 'products/join_us.html', context)
