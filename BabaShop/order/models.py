from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator
from myuser.models import CustomUser

# Create your models here.


class Order(models.Model):
    CH = "CHECKING"
    CF = "CONFIRMED"
    CA = "CANCELED"

    STATUS_CHOICES = (
        (CH, "Checking"),
        (CF, "Confirmed"),
        (CA, "Canceled"),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    total_quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CH)
    is_payment = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.id


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comment")    
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField(max_length=200)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} commented on {self.product}"


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_like")    
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'customer',)
        
        # constraints = [
        #     models.UniqueConstraint(fields=['product', 'customer'], name='like of product')
        # ]
