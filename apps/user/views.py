import re
from django.shortcuts import render, redirect
from django.urls import reverse
from validate_email import validate_email
from django.views.generic import TemplateView
from user.models import User, Address
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from celery_tasks.tasks import send_register_activation_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection


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

        send_register_activation_email.delay(email, username, token)

        return redirect(reverse('goods:index'))


class ActivationView(TemplateView):
    def get(self, request, token):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 300)

        try:
            info = serializer.loads(token)
            user_id = info["confirm"]

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse("Activation token expired")


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        """Validate login credential"""

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', { 'errmsg': 'Incomplete Data'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                redirect_to = request.GET.get('redirect_to', reverse('goods:index'))

                response = redirect(redirect_to)

                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response

            else:
                return render(request, 'login.html', {'errmsg': 'User is not activated'})

        else:
            return render(request, 'login.html', { 'errmsg': 'Wrong password'})


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)

        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'user_center_info.html'
    login_url = '/user/login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)

        con = get_redis_connection('default')
        history_key = f'history_{user.id}'

        sku_ids = con.lrange(history_key, 0, 4) # [2,3,1]

        # This way will make sure the products listed in "viewed" order, not "id" order.
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {'page':'user',
                   'address':address,
                   'goods_li':goods_li}

        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'user_center_order.html'


class AddressView(LoginRequiredMixin, TemplateView):
    template_name = 'user_center_site.html'

    def get(self, request):
        # Fetch the user from request
        user = request.user

        # Fetch user default address
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        """Add new address"""
        # Recive data
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # Validate data
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': 'Data incomplete'})

        # Validate phone number
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': 'Incorrect phone number'})

        # If user already have a default address
        # then new address will not be default, otherwise true
        # Fetch the user from request
        user = request.user

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # Add address
        Address.objects.create(
            user=user,
            receiver=receiver,
            addr=addr,
            zip_code=zip_code,
            is_default=is_default,
        )

        # Return response, refresh address page
        return redirect(reverse('user:address'))
