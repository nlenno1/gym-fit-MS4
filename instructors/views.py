from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from.models import Instructor
from .forms import InstructorForm


@login_required
def instructor_management(request):
    """ View to allow admin to view and edit the
    instructor profiles """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    instructors = Instructor.objects.all()

    for instructor in instructors:
        print(instructor.can_lead_classes)
        instructor.can_lead_classes_list = instructor.can_lead_classes.all()
        print(instructor.can_lead_classes_list)

    context = {
        'instructors': instructors,
    }

    return render(request, 'instructors/instructor_management.html', context)


@login_required
def add_an_instructor(request):
    """ View to allow admin to add an instructor """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    form = InstructorForm()

    if request.method == "POST":
        form = InstructorForm(request.POST)
        if form.is_valid():
            instructor = form.save()
            instructor.name = instructor.friendly_name.lower().replace(" ", "-")
            instructor.friendly_name = instructor.friendly_name.title()
            instructor.save()
            messages.success(request, f"Instructor Profile for \
                            {instructor.friendly_name} created")
            return redirect(reverse('instructor_management'))
        else:
            messages.error(request, "Unable to Instructor Profile. Please check \
                that the form is valid")

    context = {
        'form': form,
    }

    return render(request, 'instructors/add_an_instructor.html', context)


@login_required
def delete_instructor(request, instructor_id):
    """ View to allow Admin to delete an Instructor """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    instructor = Instructor.objects.get(id=instructor_id)

    if instructor:
        instructor.delete()
        messages.success(request, "Instructor deleted")
    else:
        messages.error(request, "Unable to find Instructor to Delete")

    return redirect(reverse('instructor_management'))
