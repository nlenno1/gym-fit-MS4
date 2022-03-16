from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass


def bag_contents(request):
    """Context processor for bag contents"""

    bag = request.session.get(
        "bag", {"class_access_package": None, "single_classes": []}
    )
    total = 0
    product_count = 0

    bag_items = {"class_access_package": None, "single_classes": []}

    if bag["class_access_package"]:
        package = get_object_or_404(
            ClassAccessPackage, pk=bag["class_access_package"]
        )
        total += package.price
        product_count += 1
        package.today_expires = date.today() + timedelta(days=package.duration)
        bag_items["class_access_package"] = package

    for item_id in bag["single_classes"]:
        exercise_class_object = get_object_or_404(
            SingleExerciseClass, pk=item_id
        )
        total += exercise_class_object.price
        product_count += 1
        bag_items["single_classes"].append(exercise_class_object)

    # Check if classes in the bag have happened yet
    now = datetime.now()
    for item in bag_items["single_classes"]:
        if item.class_date.strftime("%d:%m:%Y - ") + item.start_time.strftime(
            "%H:%M"
        ) <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            item.closed = True

    context = {
        "bag": bag,
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
    }

    return context
