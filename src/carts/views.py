from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from products.models import Variation
from .models import Cart, CartItem

# Create your views here.

class CartView(View):

    def get(self,request,*args,**kwargs):
        item_id = request.GET.get("item")
        if item_id:
            item_instance = get_object_or_404(Variation,id = item_id)
            qty = request.GET.get("qty")
            cart = Cart.objects.all()[0]
            cart_item = CartItem.objects.get_or_create(cart=cart, item = item_instance)[0]
            cart_item.quantity = 20
            print(cart_item)
        return HttpResponseRedirect("/")
