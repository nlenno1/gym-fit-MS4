from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from classes.models import ClassCategory
from .forms import ClassCategoryReviewForm


def create_a_category_review(request, category_id):
    """ View to allow users to create a review """

    category = get_object_or_404(ClassCategory, pk=category_id)
    form = ClassCategoryReviewForm

    if request.method == "POST":
        form = ClassCategoryReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.author = request.user
            new_review.review_subject = category
            new_review.save()
            messages.success(request, f"Review for {category.friendly_name} created")
            return redirect(reverse('view_single_class_category', kwargs={'category_id':category.id}))

    context = {
        'category': category,
        'form': form,
    }

    return render(request, 'reviews/write_a_category_review.html', context)
