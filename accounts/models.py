from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, surname, date_of_birth, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        ->
        """

        if not email or not name or not surname:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
            surname=surname,
        )

        user.set_password(password)
        user.save(using=self._db)  # argument rather obsolete, used in multiple database environments

        if not user.is_superuser:
            # create profile automatically and assign it to a non admin user
            p = CustomerProfile.objects.create(user=user)
            # create subscription automatically and assign it to a non admin user
            sub = Subscription.objects.create(user=user)

        return user

    def create_superuser(self, email, name, surname, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, date_of_birth=date_of_birth, name=name, surname=surname)

        user.is_superuser = True  # user with all permissions
        user.is_staff = True  # allows admin login
        user.listed_offers_limit = 1000
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    # permissions mixin gives is_superuser, groups and users_permissions

    class Meta:
        verbose_name_plural = "Custom Users"
        ordering = ["id"]

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    date_of_birth = models.DateField()
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    # 10.00 will be max can be null at first -> given by another users
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    listed_offers_limit = models.SmallIntegerField(editable=False, default=5)
    joined_on = models.DateTimeField(auto_now_add=True, editable=False)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # owners
    is_staff = models.BooleanField(
        "staff status", default=False, help_text="Designates whether the user can log into this admin " "site."
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["date_of_birth", "name", "surname"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    def rate_user(self, other_user):
        # todo method to rate another user
        pass

    def add_game(self):
        # todo implement functionality to add game for admins only or smth
        pass


class CustomerProfile(models.Model):
    """
    customer profile which is linked with every non admin user.
    -> creation in the model manager of CustomUserModel
    """

    class Meta:
        verbose_name_plural = "Customer Profiles"

    # todo signal for creation?
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    total_revenue_generated = models.IntegerField(blank=True, default=0)
    items_sold = models.SmallIntegerField(blank=True, default=0)
    items_bought = models.SmallIntegerField(blank=True, default=0)
    days_in_row = models.SmallIntegerField(
        blank=True, help_text="number of days user visited the site in a row", default=0
    )

    def __str__(self) -> str:
        return f"Profile:{self.id} User: {self.user}"


class Subscription(models.Model):
    TRIAL = "T"
    NORMAL = "N"
    SUPER = "S"
    PREMIUM = "P"
    FREE = "X"

    TYPE_CHOICES = [(TRIAL, "Trial"), (NORMAL, "Normal"), (SUPER, "Super"), (PREMIUM, "Premium"), (FREE, "Free")]

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=FREE, blank=True)
    trial_used = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    user = models.OneToOneField(
        CustomUserModel, on_delete=models.CASCADE, related_name="subscription", blank=True, null=True
    )
