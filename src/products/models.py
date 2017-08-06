from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default="This is description will show for default products")
    price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places=2,default=9.99,null=True,blank=True)
    def __str__(self):
        return self.title
