from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Hello,\n\nYour booking is confirmed!\nDetails: {booking_details}"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
