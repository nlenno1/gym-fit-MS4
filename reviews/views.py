from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from classes.models import ClassCategory
from reviews.models import ClassCategoryReview
from .forms import ClassCategoryReviewForm


@login_required
def create_a_category_review(request, category_id):
    """View to allow users to create a review"""
    # define required variables
    category = get_object_or_404(ClassCategory, pk=category_id)
    form = ClassCategoryReviewForm

    if request.method == "POST":
        # filter reviews to find if one exists from the user
        previous_review = ClassCategoryReview.objects.filter(
            author=request.user, review_subject=category
        ).exists()
        if previous_review:
            # show error message with date to help the
            # User find their previous review
            messages.error(
                request,
                f"You can't add a review as you have \
                already written one on {previous_review.friendly_created_on}",
            )
        else:
            form = ClassCategoryReviewForm(request.POST)
            if form.is_valid():  # validate form and save generated values
                new_review = form.save(commit=False)
                new_review.author = request.user
                new_review.review_subject = category
                new_review.save()
                messages.success(
                    request,
                    f"Review for \
                                 {category.friendly_name} created",
                )
            else:  # error message for invalid form
                messages.error(
                    request,
                    "Unable to create review. Please check \
                    that the form is valid",
                )

        return redirect(  # redirect to the page you came from
            reverse(
                "view_single_class_category",
                kwargs={"category_id": category.id},
            )
        )

    context = {
        "category": category,
        "form": form,
    }

    return render(request, "reviews/write_a_category_review.html", context)


@login_required
def delete_category_review(request, review_id):
    """View to allow users to delete a review"""
    # find the review if it exists
    review = get_object_or_404(ClassCategoryReview, id=review_id)
    category = review.review_subject

    if review:  # if the review is found then delete it
        review.delete()
        messages.success(request, f"Review for {category} classes deleted")
    else:  # user feedback message
        messages.error(request, f"Unable to find this review of {category} \
            to delete")

    return redirect(
        reverse(
            "view_single_class_category", kwargs={"category_id": category.id}
        )
    )
