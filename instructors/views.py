from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from.models import Instructor
from .forms import InstructorForm

@login_required
def add_an_instructor(request):
    """ View to allow admin to add an instructor """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    form = InstructorForm()

    context = {
        'form': form,
    }

    return render(request, 'instructors/add_an_instructor.html', context)


@login_required
def instructor_management(request):
    """ View to allow admin to view and edit the
    instructor profiles """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    instructors = Instructor.objects.all()

    context = {
        'instructors': instructors,
    }

    return render(request, 'instructors/instructor_management.html', context)
