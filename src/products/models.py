from django.db import models
from django.db.models.signals import pre_save, post_save
#change a slug that has a space in it to a legit slug
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True) #unique=True
    description = models.TextField(default="This is description will show for default products")
    price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99,null=True,blank=True)
    def __str__(self):
        return self.title

def product_pre_save_reciever(sender,instance, *args, **kwargs):
    print(sender)
    print(instance)
    # Let's check to make sure a slug isn't already available
    # If it is, we probably don't want to change that
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(product_pre_save_reciever, sender=Product)

""" Either way will work. Doing the slugify pre_save will be a bit cleaner
IMO, but either way will get the job done"""

# def product_post_save_reciever(sender,instance, *args, **kwargs):
#     if instance.slug !=  slugify(instance.title):
#         instance.slug = slugify(instance.title)
#         instance.save()
#
# post_save.connect(product_pre_save_reciever, sender=Product)
