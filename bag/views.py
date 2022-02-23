from django.shortcuts import render, redirect


def view_bag(request):
    """ View to render the shopping bag """

    return render(request, 'bag/bag.html')


def add_package_to_bag(request, item_id):
    """ View to add a package to the shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': None,
                                      'single_classes': []})

    bag['class_access_package'] = item_id

    request.session['bag'] = bag
    print(request.session['bag'])

    return redirect(redirect_url)


def add_single_class_to_bag(request, item_id):
    """ View to add a single class to the shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': None,
                                      'single_classes': []})

    if item_id not in bag['single_classes']:
        bag['single_classes'].append(item_id)

    request.session['bag'] = bag

    return redirect(redirect_url)
