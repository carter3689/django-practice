from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
#change a slug that has a space in it to a legit slug
from django.utils.text import slugify
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

# Overiding the standard queryset and setting active to True
    def all(self,*args,**kwargs):
        return self.get_queryset().active()

class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True) #unique=True
    description = models.TextField()
    price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99,null=True,blank=True)
    active = models.BooleanField(default = True)
    objects = ProductManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail_slug_view", kwargs = {"slug":self.slug})

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

class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99,null=True,blank=True)
    active = models.BooleanField(default = True)
    inventory = models.IntegerField(null=True,blank=True) # This will allow for unlimited Inventory if left blank

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

def product_variatin_post_save_receiver(sender,instance,created,*args,**kwargs):
    print(sender)
    print(instance)

    product = instance #The Product that was saved/created (eg airjordan5)
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_variation = Variation()
        new_variation.product = product
        new_variation.title = "Default"
        new_variation.price = product.price
        new_variation.save()

    print(created)

post_save.connect(product_variatin_post_save_receiver, sender = Product)


# Product Images

def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/%s" %(slug, new_filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title
