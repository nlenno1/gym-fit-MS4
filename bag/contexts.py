from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass

def bag_contents(request):
    """ Context processor for bag contents"""

    bag = request.session.get('bag', {'class_access_package': {"item_id": None, "package_object": None},
                                      'single_classes': []})
    total = 0
    product_count = 0

    if bag['class_access_package']['item_id']:
        package = get_object_or_404(ClassAccessPackage, pk=bag['class_access_package']['item_id'])
        total += package.price
        product_count += 1
        package.today_expires = date.today() + timedelta(days=package.duration)
        bag['class_access_package']['package_object'] = package

    for item in bag['single_classes']:
        exercise_class_object = get_object_or_404(SingleExerciseClass, pk=item['item_id'])
        total += exercise_class_object.price
        product_count += 1
        exercise_class_object.start_time = exercise_class_object.start_time.strftime('%H:%M')
        exercise_class_object.end_time = exercise_class_object.end_time.strftime('%H:%M')
        item['exercise_class_object'] = exercise_class_object

    context = {
        'bag': bag,
        'total': total,
        'product_count': product_count,
    }

    print(context)

    return context
