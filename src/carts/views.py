from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect,Http404,JsonResponse
from django.shortcuts import render,get_object_or_404

from products.models import Variation
from .models import Cart, CartItem

# Create your views here.

class CartView(SingleObjectMixin,View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self,*args,**kwargs):
        self.request.session.set_expiry(0) # This will end the session when the user closes their browser.
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart.id
        cart = Cart.objects.get(id = cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart


    def get(self,request,*args,**kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete",False) # Default for deleted items will be set to False.
        item_added = False # Default for added items
        if item_id:
            item_instance = get_object_or_404(Variation,id = item_id)
            qty = request.GET.get("qty",1) #Giving the quantity a default value of 1
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item,created_item= CartItem.objects.get_or_create(cart=cart, item = item_instance) # We will either have a created item, or an item that is already in the cart
            if created_item:
                item_added = True # If a new item is added to the cart it will return as True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
                print(cart_item)
        if request.is_ajax(): # If an AJAX call happens then...
            print(request.GET.get("item")) # Then print out what the request gives back
            return JsonResponse({"deleted":delete_item,"created":item_added}) # Return a JSON Response.
        context = {
            "object":self.get_object()
        }
        print(context)
        template = self.template_name
        return render(request,template,context)
