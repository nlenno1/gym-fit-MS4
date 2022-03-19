from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass


def bag_contents(request):
    """Context processor for bag contents"""
    # get the bag fromt he session storage
    bag = request.session.get(
        "bag", {"class_access_package": None, "single_classes": []}
    )
    # set variables for storage
    total = 0
    product_count = 0
    bag_items = {"class_access_package": None, "single_classes": []}
    now = datetime.now()

    # find the package using storage data, save the cost amount to the total,
    # set the package expiry date and increment the product count
    if bag["class_access_package"]:
        package = get_object_or_404(
            ClassAccessPackage, pk=bag["class_access_package"]
        )
        total += package.price
        product_count += 1
        package.today_expires = date.today() + timedelta(days=package.duration)
        bag_items["class_access_package"] = package
    # for the items in the single classes list, find the class
    # add the cost amount to the total, increment the product count
    for item_id in bag["single_classes"]:
        exercise_class_object = get_object_or_404(
            SingleExerciseClass, pk=item_id
        )
        total += exercise_class_object.price
        product_count += 1
        # check if class has started
        if exercise_class_object.class_date.strftime(
                "%d:%m:%Y - ") + exercise_class_object.start_time.strftime(
                "%H:%M") <= now.strftime("%d:%m:%Y - %H:%M:%S"):
            exercise_class_object.closed = True
        bag_items["single_classes"].append(exercise_class_object)
        # sort single classes in the bag items by date and start time
        bag_items["single_classes"] = sorted(
                bag_items["single_classes"], key=lambda d: (
                    d.class_date, d.start_time))

    context = {
        "bag": bag,
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
    }

    return context
