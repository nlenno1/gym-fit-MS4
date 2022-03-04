from datetime import date, timedelta
from django.shortcuts import render

from profiles.models import UserProfile
from .models import ClassAccessPackage
from .forms import ClassAccessPackageForm


def view_class_access_packages(request):
    """ A view to return the class access packages available"""

    packages = ClassAccessPackage.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    profile.check_package_expired()

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
        'profile': profile,
    }

    return render(request, 'products/join_us.html', context)


def add_class_access_package(request):
    """ A view to allow Admin to add new packages"""

    form = ClassAccessPackageForm()

    context = {
        'form': form,
    }

    return render(request, 'products/add_class_access_package.html', context)
