from django.shortcuts import render

from instructors.models import Instructor

def index(request):
    """ View to render home page """

    instructors = Instructor.objects.all()

    context = {
        'instructors': instructors
    }

    return render(request, 'home/index.html', context)
