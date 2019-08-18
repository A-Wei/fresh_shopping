from django.urls import path
from goods.views import IndexView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index'), # This should be replace by celery static index page
]
