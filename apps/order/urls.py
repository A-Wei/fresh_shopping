from django.urls import path
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView,CommentView

urlpatterns = [

    path('place', OrderPlaceView.as_view(), name='place'), # 提交订单信息
]
