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
    
    username_regex = RegexValidator(regex = r'^[\w.+-]*[a-zA-Z][\w.+-]*\Z', message="username must contain at least one letter; @ is not accepted")
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and ./+/-/_ only. At least One letter is necessary'),
        validators=[username_regex],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

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

    if phone:
        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = [ 'username', 'email']
    elif email:
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = [ 'username', 'phone']
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
