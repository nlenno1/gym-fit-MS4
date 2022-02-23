from django.shortcuts import render, redirect


def view_bag(request):
    """ View to render the shopping bag """

    return render(request, 'bag/bag.html', )


def add_package_to_bag(request, item_id):
    """ View to add a package to the shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': {"item_id": None, "package_object": None},
                                      'single_classes': []})

    bag['class_access_package']['item_id'] = item_id

    request.session['bag'] = bag

    return redirect(redirect_url)


def add_single_class_to_bag(request, item_id):
    """ View to add a single class to the shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {'class_access_package': {"item_id": None},
                                      'single_classes': []})

    if len(bag['single_classes']) > 0:
        if not any(item['item_id'] == item_id for item in bag['single_classes']):
            bag['single_classes'].append({
                'item_id': item_id
            })
    else:
        bag['single_classes'].append({
            'item_id': item_id
        })

    request.session['bag'] = bag

    return redirect(redirect_url)
