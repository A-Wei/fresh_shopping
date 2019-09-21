from django.urls import path
from cart.views import CartAddView, CartInfoView

urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),
    path('', CartInfoView.as_view(), name='show'),
]
