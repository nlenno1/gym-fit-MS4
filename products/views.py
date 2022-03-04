from datetime import date, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


@login_required
def add_class_access_package(request):
    """ A view to allow Admin to add new package """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    if request.method == "POST":
        form = ClassAccessPackageForm(request.POST, request.FILES)
        if form.is_valid():
            if form['type'] == "TK":
                form.duration = 86
            elif form['type'] == "UU":
                form.amount_of_tokens = None
            form.save()
            messages.success(request, "Successfully Created A \
                             Class Access Package")
            return redirect(reverse('view_class_access_package'))
        else:
            messages.error(request, "Failed to create the Class Access Package\
                           . Please ensure the form is valid")
    else:
        form = ClassAccessPackageForm()

    context = {
        'form': form,
    }

    return render(request, 'products/add_class_access_package.html', context)


@login_required
def edit_class_access_package(request, package_id):
    """ A view to allow Admin to edit a package """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    package = get_object_or_404(ClassAccessPackage, id=package_id)

    if request.method == "POST":
        form = ClassAccessPackageForm(request.POST, request.FILES,
                                      instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated Class Access \
                             Package")
            return redirect(reverse('view_class_access_packages'))
        else:
            messages.error(request, "Failed to update Class Access \
                           Package. Please ensure the form is valid")
    else:
        form = ClassAccessPackageForm(instance=package)
        messages.info(request, f'You are now editing the Class Access Package \
                      called "{package.friendly_name}"')

    context = {
        'form': form,
        'package': package,
    }

    return render(request, 'products/edit_class_access_package.html', context)


@login_required
def delete_class_access_package(request, package_id):
    """ A view to allow Admin to delete a package """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    package = get_object_or_404(ClassAccessPackage, id=package_id)
    package.delete()
    messages.success(request, "Package deleted")
    return redirect(reverse('view_class_access_packages'))
