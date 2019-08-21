from django.urls import path
from goods.views import IndexView, DetailView, ListView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index'), # This should be replace by celery static index page
    path('goods/<int:goods_id>', DetailView.as_view(), name='detail'),
    path('goods/<int:type_id>/<int:page>/', ListView.as_view(), name='list'),
]
