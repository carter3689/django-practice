from django.db import models
from django.conf import settings
# Create your models here.
class GuestCheckout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null= True, blank = True)
    email = models.EmailField()
    #merchant_id

    def __str__(self):
        return self.email


# class Order(models.Model):
#     #cart
#     #user checkout ==> required
#     #guest noe required
#     #shipping address
#     #billing address
#     #shipping total price
#     # order totoal (cart total + shipping)
#     #order_id --> custom_id
