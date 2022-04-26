from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class AccountManagerCustom(BaseUserManager):

    def create_user(self,
                    email,
                    username,
                    first_name,
                    last_name,
                    birthdate,
                    addr_city,
                    addr_street,
                    addr_post_code,
                    mobile_nr,
                    password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not birthdate:
            raise ValueError("User must have a birthdate")
        if not addr_city:
            raise ValueError("User must have a city")
        if not addr_street:
            raise ValueError("User must have a street")
        if not addr_post_code:
            raise ValueError("User must have a post code")
        if not mobile_nr:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            addr_city=addr_city,
            addr_street=addr_street,
            addr_post_code=addr_post_code,
            mobile_nr=mobile_nr
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         username,
                         first_name,
                         last_name,
                         birthdate,
                         addr_city,
                         addr_street,
                         addr_post_code,
                         mobile_nr,
                         password):

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            addr_city=addr_city,
            addr_street=addr_street,
            addr_post_code=addr_post_code,
            mobile_nr=mobile_nr)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self.db)
        return user


class UserCustom(AbstractBaseUser):

    email = models.EmailField(verbose_name="Email", max_length=50, unique=True)
    username = models.CharField(verbose_name="Username", max_length=25, unique=True)
    join_date = models.DateTimeField(verbose_name="Join date", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)

    first_name = models.CharField(verbose_name="First name", max_length=30)
    last_name = models.CharField(verbose_name="Last name", max_length=50)
    birthdate = models.DateField(verbose_name="Date of birth")
    addr_city = models.CharField(verbose_name="City", max_length=30)
    addr_street = models.CharField(verbose_name="Street", max_length=100)
    addr_post_code = models.CharField(verbose_name="Post code", max_length=25)
    mobile_nr = models.CharField(verbose_name="Mobile", max_length=15)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManagerCustom()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'first_name',
                       'last_name',
                       'birthdate',
                       'addr_city',
                       'addr_street',
                       'addr_post_code',
                       'mobile_nr'
                       ]

    def __str__(self):
        return f"{self.username} mail: {self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
