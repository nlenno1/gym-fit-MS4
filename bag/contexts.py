from django.shortcuts import get_object_or_404
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass

def bag_contents(request):
    """ Context processor for bag contents"""

    bag = request.session.get('bag', {'class_access_package': {'item_id': None},
                                      'single_classes': []})
    total = 0
    product_count = 0

    print(bag)

    if bag['class_access_package']['item_id']:
        package = get_object_or_404(ClassAccessPackage, pk=bag['class_access_package']['item_id'])
        total += package.price
        product_count += 1
        bag['class_access_package']['package_object'] = package

    for item in bag['single_classes']:
        exercise_class_object = get_object_or_404(SingleExerciseClass, pk=item['item_id'])
        total += exercise_class_object.price
        product_count += 1
        item['exercise_class_object'] = exercise_class_object

    context = {
        'bag': bag,
        'total': total,
        'product_count': product_count,
    }

    print(context)

    return context
