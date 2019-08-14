from django.urls import path
from user.views import RegisterView, ActivationView, LoginView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('active/<token>/', ActivationView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name='login')
]
