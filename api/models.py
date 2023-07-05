from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from api.validators import release_date_validator


class RetailObjectType(models.TextChoices):
    FACTORY = "FA", _("Factory")
    DISTRIBUTOR = "DI", _("Distributor")
    LRC = "LRC", _("Large retail chain")
    DECEMBER = "DE", _("Dealership")
    IE = "IE", _("Individual entrepreneur")


class RetailObject(models.Model):
    """Electronics retail chain model."""

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    contact = models.OneToOneField(
        "Contact",
        related_name="object",
        on_delete=models.CASCADE,
        verbose_name=_("Contact"),
    )
    product = models.ManyToManyField(
        "Product", related_name="object", verbose_name=_("Product")
    )
    employee = models.ForeignKey(
        "Employee",
        related_name="object",
        verbose_name=_("Employee"),
        on_delete=models.CASCADE,
    )
    provider = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="object",
        verbose_name=_("Provider"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Сreation time")
    )
    level = models.IntegerField(default=0)
    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        null=True,
        verbose_name=_("Supplier debt"),
    )
    type = models.CharField(
        max_length=20,
        choices=RetailObjectType.choices,
        default=RetailObjectType.FACTORY,
        verbose_name=_("Retail chain type"),
    )

    def provider_link(self):
        if self.provider is None:
            return format_html("<a>None</a>")
        return format_html(
            '<a href="%s">%s</a>'
            % (
                reverse("admin:api_retailobject_change", args=(self.provider.id,)),
                escape(self.provider.name),
            )
        )

    provider_link.allow_tags = True
    provider_link.short_description = "Provider"

    def calculate_level(self):
        if self.type == RetailObjectType.FACTORY:
            return 0

        if self.provider is None:
            return 0

        retail_object = RetailObject.objects.get(id=self.provider.id)
        return retail_object.level + 1

    def save(self, *args, **kwargs):
        self.level = self.calculate_level()
        super(RetailObject, self).save(*args, **kwargs)


class Contact(models.Model):
    """Contact model."""

    email = models.EmailField(max_length=50, unique=True, verbose_name=_("Email"))
    address = models.OneToOneField(
        "Address",
        related_name="contacts",
        on_delete=models.CASCADE,
        verbose_name=_("Address"),
    )


class Address(models.Model):
    """Address model."""

    country = models.CharField(max_length=50, verbose_name=_("Country"))
    city = models.CharField(max_length=50, verbose_name=_("City"))
    street = models.CharField(max_length=50, verbose_name=_("Street"))
    house_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_("House Number")
    )

    class Meta:
        verbose_name = "Addres"


class Product(models.Model):
    """Product model."""

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    product_model = models.CharField(max_length=25, verbose_name=_("Product Model"))
    release_date = models.DateTimeField(
        verbose_name=_("Market launch date"),
        validators=[release_date_validator],
        null=True,
    )


class Employee(AbstractUser):
    """Employee model."""

    first_name = models.CharField(max_length=25, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=25, verbose_name=_("Last Name"))
    email = models.EmailField(max_length=50, unique=True, verbose_name=_("Email"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of hire"))

    class Meta:
        verbose_name = "Employee"
