from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
import random

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="Phone number must be entered in the format: '+989121234567'.")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True) # validators should be a list
    
    image = models.ImageField(upload_to='user_image/', default='user_image/avatar.jpg', null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)

    is_customer = models.BooleanField(
        _('customer status'),
        default=False,
        help_text=_('Designates whether the user can log as a customer.'),
    )
    is_supplier = models.BooleanField(
        _('supplier status'),
        default=False,
        help_text=_('Designates whether the user can log as a supplier.'),
    )

    if email:
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = [ 'username', 'phone']
    elif phone:
        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = [ 'username', 'email']
    else:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = [ 'phone', 'email']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class Address(models.Model):
    slug = models.SlugField(max_length=70, blank=True, unique=True)
    label = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=230)
    zipcode = models.CharField(max_length=10)
    customer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="customer_address")

    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.label) + '_address'
            while Address.objects.filter(slug = self.slug):
                self.slug = slugify(self.label)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.label
