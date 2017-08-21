from django.db import models
from django.conf import settings


from carts.models import Cart
# Create your models here.
class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null= True, blank = True)
    email = models.EmailField(unique = True)
    #merchant_id

    def __str__(self):
        return self.email

    # def get_client_token(self):
    #     customer_id = self.get_braintree_id
    #     if customer_id:
    #         client_token = braintree.ClientToken.generate({
	# 		    "customer_id": customer_id
	# 		})
	# 		return client_token
	# 	return None

ADDRESS_TYPE = (
    ('billing', 'billing'),
    ('shipping', 'shipping'),
)

class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length = 120)
    zipcode = models.CharField(max_length=120)


    def __str__(self):
        return self.street

class Order(models.Model):
	cart = models.ForeignKey(Cart)
	user = models.ForeignKey(UserCheckout)
	billing_address = models.ForeignKey(UserAddress, related_name='billing_address')
	shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address')
	shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
	order_total = models.DecimalField(max_digits=50, decimal_places=2, )
	#order_id

	def __unicode__(self):
		return str(self.cart.id)
