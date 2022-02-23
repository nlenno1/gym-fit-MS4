def bag_contents(request):
    """ Context processor for bag contents"""

    bag_items = {
        'class_access_package': None,
        'single_classes': [],
    }
    total = 0
    product_count = 0

    product_count = len(bag_items['single_classes'])
    if bag_items['class_access_package']:
        product_count += 1

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context
