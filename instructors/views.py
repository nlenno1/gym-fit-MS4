from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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