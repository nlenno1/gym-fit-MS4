from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass

def view_bag(request):
    """ View to render the shopping bag """

    return render(request, 'bag/bag.html', )


def add_package_to_bag(request, item_id):
    """ View to add a package to the shopping bag """

    package = get_object_or_404(ClassAccessPackage, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': None,
                                    'single_classes': []})

    bag['class_access_package'] = item_id

    messages.success(request, f'Added {package.friendly_name} to your shopping bag')

    request.session['bag'] = bag

    return redirect(redirect_url)


def add_single_class_to_bag(request, item_id):
    """ View to add a single class to the shopping bag """

    exercise_class = get_object_or_404(SingleExerciseClass, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': None,
                                     'single_classes': []})

    if item_id not in bag['single_classes']:
        bag['single_classes'].append(item_id)
        messages.success(request, f'Added {exercise_class.category} at {exercise_class.start_time} on {exercise_class.date} to your shopping bag')
    else:
        messages.warning(request, f'{exercise_class.category} at {exercise_class.start_time} on {exercise_class.date} is already in your shopping bag')

    request.session['bag'] = bag

    return redirect(redirect_url)


def remove_from_bag(request, product_type, item_id):
    """ View to remove items from the bag """

    bag = request.session.get('bag', {'class_access_package': None,
                                      'single_classes': []})

    if product_type == 'package':
        bag['class_access_package'] = None
    elif product_type == 'single_class':
        bag['single_classes'].remove(item_id)

    return redirect(reverse('view_bag'))
