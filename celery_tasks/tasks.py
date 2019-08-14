from celery import Celery
from django.core.mail import send_mail
from django.template import loader
from celery import shared_task
from fresh_shopping.settings import BASE_URL


@shared_task
def send_register_activation_email(to_email, username, token):
    html_message = loader.render_to_string(
            "activation.html",
            {
                "username": username,
                "base_url": str(BASE_URL),
                "token": token,
            },
        )
    recipient = to_email

    send_mail(
        subject="Activate your email",
        message="",
        from_email="<rsvp@freshshopping.com>",
        recipient_list=[recipient],
        fail_silently=False,
        html_message=html_message,
    )
