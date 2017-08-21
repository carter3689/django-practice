from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin,DetailView
from django.http import HttpResponseRedirect,Http404,JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.edit import FormMixin

from products.models import Variation
from .models import Cart, CartItem
from orders.models import UserCheckout, Order, UserAddress
from orders.forms import GuestCheckoutForm
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
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))
        if request.is_ajax(): # If an AJAX call happens then...
            print(request.GET.get("item")) # Then print out what the request gives back
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart_subtotal
            except:
                subtotal = None
            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal":subtotal,
            }
            return JsonResponse(data) # Return a JSON Response.
        context = {
            "object":self.get_object()
        }
        template = self.template_name
        return render(request,template,context)



class CheckoutView(FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout_view.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return redirect("cart")
		cart = Cart.objects.get(id=cart_id)
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super(CheckoutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_check_id = self.request.session.get("user_checkout_id")
		if not self.request.user.is_authenticated() or user_check_id == None:# or if request.user.is_guest:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		elif self.request.user.is_authenticated() or user_check_id != None:
			user_can_continue = True
			#return redirect "address select view"
		else:
			pass
		if self.request.user.is_authenticated():
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			self.request.session["user_checkout_id"] = user_checkout.id

		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse("checkout")


	def get(self, request, *args, **kwargs):
		get_data = super(CheckoutView, self).get(request, *args, **kwargs)
		cart = self.get_object()
		user_checkout_id = request.session.get("user_checkout_id")
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			billing_address_id = request.session.get("billing_address_id")
			shipping_address_id = request.session.get("shipping_address_id")

			if billing_address_id == None or shipping_address_id == None:
				return redirect("address_form")
			else:
				billing_address = UserAddress.objects.get(id=billing_address_id)
				shipping_address = UserAddress.objects.get(id=shipping_address_id)

			try:
				new_order_id = request.session["order_id"]
				new_order = Order.objects.get(id=new_order_id)
			except:
				new_order = Order()
				request.session["order_id"] = new_order.id

			new_order.cart = cart
			new_order.user = user_checkout
			new_order.billing_address = billing_address
			new_order.shipping_address = shipping_address
			new_order.save()
		return get_data
