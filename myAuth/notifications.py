# Notify me when users sign up or confirm email
from allauth.account.signals import email_confirmed, user_signed_up
from decouple import config
from django.core.mail import send_mail
from django.dispatch import receiver


@receiver(user_signed_up, dispatch_uid="user_signed_up_receiver")
def notify_user_signed_up(sender, **kwargs):
    # print(f"Oh shit, {kwargs['user']} is signing up!")
    send_mail(
        "DOOR2DOOR - NEW USER SIGNUP",
        f"{kwargs['user']} has just signed up for door2door",
        config("EMAIL_HOST_USER"),
        [config("EMAIL_HOST_USER")],
        fail_silently=False,
    )


@receiver(email_confirmed, dispatch_uid="notify_email_confirmed_receiver")
def notify_email_confirmed(sender, **kwargs):
    # print(f"Oh shit, {kwargs['email_address']} just got confirmed!")
    send_mail(
        "DOOR2DOOR - EMAIL CONFIRMED",
        f"{kwargs['email_address']} has just been confirmed!",
        config("EMAIL_HOST_USER"),
        [config("EMAIL_HOST_USER")],
        fail_silently=False,
    )
