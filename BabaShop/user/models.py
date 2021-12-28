from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('email address'), max_length=13, unique=True)
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

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
