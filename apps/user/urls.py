from django.urls import path
from user.views import (
    RegisterView,
    ActivationView,
    LoginView,
    UserInfoView,
    UserOrderView,
    AddressView,
    LogoutView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('active/<token>/', ActivationView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name='login'),
    path('', UserInfoView.as_view(), name='user'),
    path('order/', UserOrderView.as_view(), name='order'),
    path('address/', AddressView.as_view(), name='address'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
