from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse # Ajex returns json object
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
# Create your views here.

class CartAddView(View):
    """Add sku to cart"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            #If user not logged in
            return JsonResponse({'res': 0, 'errmsg': 'Please login first'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # Data validation
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': 'Data incomplete'})

        # Update count
        try:
            count = int(count)
        except Exception:
            return JsonResponse({'res': 2, 'errmsg': 'Count number incorrect'})

        # Validate goods id
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception:
            return JsonResponse({'res': 3, 'errmsg': 'Goods not found'})

        conn = get_redis_connection('default')
        cart_key  = 'cart_%d'%user.id
        # hash data structure 'cart_key': {'sku_id': count, 'sku_id2': count}
        cart_count = conn.hget(cart_key, sku_id)

        if cart_count:
            count += int(cart_count)

        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': 'Not enough in stock'})

        conn.hset(cart_key, sku_id, count)

        total_count = conn.hlen(cart_key)

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': 'Sucess'})

class CartInfoView(LoginRequiredMixin, View):
    '''购物车页面显示'''
    def get(self, request):
        '''显示'''
        # 获取登录的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 动态给sku对象增加一个属性amount, 保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count, 保存购物车中对应商品的数量
            sku.count = count
            # 添加
            skus.append(sku)

            # 累加计算商品的总数目和总价格
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {'total_count':total_count,
                   'total_price':total_price,
                   'skus':skus}

        # 使用模板
        return render(request, 'cart.html', context)
