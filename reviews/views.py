from django.shortcuts import render, get_object_or_404

from classes.models import ClassCategory
from .forms import ReviewForm


def create_a_category_review(request, category_id):
    """ View to allow users to create a review """

    category = get_object_or_404(ClassCategory, pk=category_id)
    form = ReviewForm

    context = {
        'category': category,
        'form': form,
    }

    return render(request, 'reviews/write_a_category_review.html', context)
