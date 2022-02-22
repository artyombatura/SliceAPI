from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Photo(models.Model):
    url = models.URLField(max_length=255)


class User(AbstractBaseUser, PermissionsMixin):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(_("username"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    email = models.EmailField(_("email"), unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    is_active = models.BooleanField(_("active status"), default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Restaurant(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(
        _("description"),
    )
    address = models.CharField(_("address"), max_length=255)
    phone_number = models.CharField(_("phone_number"), max_length=255)

    def __str__(self):
        return self.name


class LastVisitedRestaurants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="visit"
    )
    date = models.DateTimeField(_("date"), default=timezone.now)

    def __str__(self):
        return f"{self.user}, {self.restaurant}"


class Country(models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.CharField(_("description"), max_length=255)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(
        _("description"),
    )
    weight = models.DecimalField(_("weight"), max_digits=8, decimal_places=2)
    price = models.DecimalField(_("price"), max_digits=8, decimal_places=2)
    estimated_time = models.IntegerField(_("estimated time"))
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "dishes"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Delayed", "Delayed"),
        ("Done", "Done"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through="OrderDish")
    date = models.DateTimeField(_("date"), default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user}, {self.date}"


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(_("number"), max_length=64)
    expiration_date = models.CharField(_("expiration date"), max_length=32)
    cvv = models.CharField(_("cvv"), max_length=32)

    def __str__(self):
        return f"{self.user}, {self.number}"
