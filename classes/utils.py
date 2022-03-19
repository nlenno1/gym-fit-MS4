from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

from .models import SingleExerciseClass


def send_class_cancellation_email(exercise_class, user_profile, refunded):
    """Send the user a class cancellation email"""

    subject = render_to_string(
        "classes/cancellation_emails/cancellation_email_subject.txt",
        {"class": exercise_class},
    )
    body = render_to_string(
        "classes/cancellation_emails/cancellation_email_body.txt",
        {
            "user": user_profile,
            "contact_email": settings.DEFAULT_FROM_EMAIL,
            "class": exercise_class,
            "refunded": refunded,
        },
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [
            user_profile.email,
        ],
    )


def send_update_email(class_id, form, request):
    """Send the user a class update email"""
    exercise_class = SingleExerciseClass.objects.get(id=class_id)
    total_emails_sent = 0
    for person in exercise_class.participants.all():
        user = User.objects.get(id=person.id)

        subject = render_to_string(
            "classes/update_emails/update_email_subject.txt",
            {"class": exercise_class},
        )
        body = render_to_string(
            "classes/update_emails/update_email_body.txt",
            {
                "user": user,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
                "class": exercise_class,
                "form": form,
            },
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [
                user.email,
            ],
        )
        total_emails_sent += 1
    messages.info(request, f"Emails sent to all {total_emails_sent} \
        class participants")


def convert_ability_level_to_str(exercise_class):
    """ Function to convert the stored Abilty Level key to a string """
    if exercise_class.ability_level == "BEG":
        exercise_class.ability_level = "Beginner"
    elif exercise_class.ability_level == "INT":
        exercise_class.ability_level = "Intermediate"
    elif exercise_class.ability_level == "ADV":
        exercise_class.ability_level = "Advanced"
    else:
        exercise_class.ability_level = "For All"
