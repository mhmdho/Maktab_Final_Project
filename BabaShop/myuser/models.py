from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.core.validators import RegexValidator

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="Phone number must be entered in the format: '+989121234567'.")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True) # validators should be a list
    
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
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

    USERNAME_FIELD = 'phone' # phone/email/username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class Address(models.Model):
    lable = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10)
    customer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="customer_address")
