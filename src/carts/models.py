from django.conf import settings
from django.db import models

from products.models import Variation
# Create your models here.

class CartItem(models.Model):
    """
    # Here we use the quotes around the Cart because we haven't specifically made this available yet. But Django will take care of this once it sees the Cart class.
    """
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=2)
    # We may also want a line item (item *quantity) in the future..

    def __str__(self):
        return self.item.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null= True, blank = True)
    items = models.ManyToManyField(Variation, through=CartItem) # We will break this up later.
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return str(self.id) # Cast the ID of the cart as a string when returned.
    # Associate to a user
    # Items in Cart
    # timestamp
    # updated

    # subtotal price
    # taxes total
    # discounts (if any)
    # total price
