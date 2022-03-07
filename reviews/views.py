from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from classes.models import ClassCategory
from reviews.models import ClassCategoryReview
from .forms import ClassCategoryReviewForm


def create_a_category_review(request, category_id):
    """ View to allow users to create a review """

    category = get_object_or_404(ClassCategory, pk=category_id)
    form = ClassCategoryReviewForm

    previous_review = None
    previous_review = ClassCategoryReview.objects.get(
                      author=request.user, review_subject=category)
    previous_review.created_on = previous_review.created_on.strftime("%d %B %Y")

    if request.method == "POST":
        if previous_review:
            messages.error(request, f"You can't add a review as you have \
                already written one on {previous_review.created_on}")
        else:
            form = ClassCategoryReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.author = request.user
                new_review.review_subject = category
                new_review.save()
                messages.success(request, f"Review for \
                                 {category.friendly_name} created")
            else:
                messages.error(request, "Unable to create review. Please check \
                    that the form is valid")

        return redirect(reverse('view_single_class_category', kwargs={
                                'category_id': category.id}))

    context = {
        'category': category,
        'form': form,
    }

    return render(request, 'reviews/write_a_category_review.html', context)


def delete_category_review(request, review_id):
    """ View to allow users to delete a review """

    review = ClassCategoryReview.objects.get(id=review_id)
    category = review.review_subject

    if review:
        review.delete()
        messages.success(request, "Review deleted")
    else:
        messages.error(request, "Unable to find review to delete")

    return redirect(reverse('view_single_class_category', kwargs={'category_id':category.id}))

