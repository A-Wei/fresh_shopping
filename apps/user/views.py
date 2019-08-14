import re
from django.shortcuts import render, redirect
from django.urls import reverse
from validate_email import validate_email
from django.views.generic import TemplateView
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail


class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': 'Missing info'})

        valid_email = validate_email(email, verify=True)

        if not valid_email:
            return render(request, 'register.html', { 'errmsg': 'Invalid Email'})

        if allow != 'on':
            return render(request, 'register.html', { 'errmsg': 'Please agree terms'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', { 'errmsg': 'User already exist' })

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 300)
        info = {'confirm': user.id }
        token = serializer.dumps(info)
        token = token.decode('utf-8')

        subject = "Welcome to Fresh Shopping"
        html_message = "<h1>Message sent</h1>"
        from_email = "<rsvp@163.com>"
        recrecipient = user.email

        send_mail(
            subject=subject,
            message="",
            from_email=from_email,
            recipient_list=[recrecipient],
            fail_silently=False,
            html_message=html_message,
        )

        return redirect(reverse('goods:index'))


class ActivationView(TemplateView):
    def get(self, request, token):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 300)

        try:
            info = serializer.loads(token)
            user_id = info["confirm"]

            user = User.objects.get(id=user_id)
            user.active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse("Activation token expired")


class LoginView(TemplateView):
    template_name = 'login.html'
