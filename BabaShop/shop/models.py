from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField, CharField
from .managers import UndeletedShop, DeletedShop
from myuser.models import CustomUser

# Create your models here.


class Shop(models.Model):
    SUP = "SUPERMARKET"
    HYP = "HYPERMARKET"
    GRE = "GREENGROCER"
    FRU = "FRUIT STORE"
    ORG = "ORGANIC STORE"
    CON = "CONVENIENCE STORE"

    TYPE_CHOICES = (
        (SUP, "Supermarket"),
        (HYP, "Hypermarket"),
        (GRE, "Greengrocer"),
        (FRU, "fruit store"),
        (ORG, "Organic store"),
        (CON, "Convenience store"),
    )
    name = CharField(max_length=50)
    type = models.CharField(max_length=17, choices=TYPE_CHOICES, default=SUP)
    address = CharField(max_length=200)
    supplier = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    is_confirmed = BooleanField(default=False)
    is_deleted = BooleanField(default=False)

    objects = models.Manager()
    Deleted = DeletedShop()
    Undeleted = UndeletedShop()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=400)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE) 
    tag = models.ManyToManyField('ProductTag', blank=True)
    # like = models.IntegerField(default=0, null=True, blank=True)
    # image = models.ImageField(upload_to='product_image/')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    # objects = models.Manager()
    # Confirmed = ConfirmedProduct()
    # Unconfirmed = UnconfirmedProduct()

    class Meta:
        ordering = ['-id']

    def get_image(self):
        return self.image_set.all()

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_img")
    image = models.ImageField(upload_to='product_image/')
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.id


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class ProductTag(models.Model):
    title = models.CharField(max_length=50)

    class Meta : 
        verbose_name_plural = "pro_tags"
        verbose_name = "pro_tag"
        ordering = ['title',]
        
    def __str__(self):
        return self.title
