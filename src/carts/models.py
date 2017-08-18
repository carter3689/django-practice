from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from products.models import Variation
# Create your models here.

class CartItem(models.Model):
    """
    # Here we use the quotes around the Cart because we haven't specifically made this available yet. But Django will take care of this once it sees the Cart class.
    """
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)
    # We may also want a line item (item *quantity) in the future..

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()
        #"%s/?item=%s&delete=True" % (reverse("cart"),self.item.id) # This REGEX is looking for a DELETE URL associated with our CART URL.


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if int(qty) >= 1:
		price = instance.item.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null= True, blank = True)
    items = models.ManyToManyField(Variation, through=CartItem) # We will break this up later.
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2,default=0.00)

    def __str__(self):
        return str(self.id) # Cast the ID of the cart as a string when returned.

    def update_subtotal(self):
        print("updating...")
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += items.line_item_total
        self.subtotal = subtotal
        print(self.subtotal)
        self.save()


    # Associate to a user
    # Items in Cart
    # timestamp
    # updated

    # subtotal price
    # taxes total
    # discounts (if any)
    # total price
