from celery import Celery
from django.core.mail import send_mail
from django.template import loader
from celery import shared_task
from fresh_shopping.settings import BASE_URL


@shared_task
def send_register_activation_email(to_email, username, token):
    subject = f"{ username }, Welcome to Fresh Shopping"
    html_message = loader.render_to_string(
            "activation.html",
            {
                "base_url": str(BASE_URL),
                "token": token,
            },
        )
    from_email = "<rsvp@example.com>"
    recrecipient = to_email

    send_mail(
        subject=subject,
        message="",
        from_email=from_email,
        recipient_list=[recrecipient],
        fail_silently=False,
        html_message=html_message,
    )
