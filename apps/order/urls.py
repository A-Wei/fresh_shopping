from django.urls import path
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView,CommentView

urlpatterns = [

    path('place', OrderPlaceView.as_view(), name='place'), # 提交订单信息
    path('commit', OrderCommitView.as_view(), name='commit'), # 订单创建
]
