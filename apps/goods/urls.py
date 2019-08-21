from django.urls import path
from goods.views import IndexView, DetailView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index'), # This should be replace by celery static index page
    path('goods/<int:goods_id>', DetailView.as_view(), name='detail')
]
