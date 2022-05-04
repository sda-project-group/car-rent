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
    username = models.CharField(verbose_name="Nazwa uzytkownika", max_length=25, unique=True)
    join_date = models.DateTimeField(verbose_name="Data dolaczenia", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Ostatnie logowanie", auto_now=True)

    first_name = models.CharField(verbose_name="Imie", max_length=30)
    last_name = models.CharField(verbose_name="Nazwisko", max_length=50)
    birthdate = models.DateField(verbose_name="Data urodzenia")
    addr_city = models.CharField(verbose_name="Miasto", max_length=30)
    addr_street = models.CharField(verbose_name="Ulica", max_length=100)
    addr_post_code = models.CharField(verbose_name="Kod pocztowy", max_length=25)
    mobile_nr = models.CharField(verbose_name="Nr telefonu", max_length=15)

    is_admin = models.BooleanField(verbose_name="Administrator", default=False)
    is_staff = models.BooleanField(verbose_name="Pracownik", default=False)
    is_superuser = models.BooleanField(verbose_name="Glowny administrator", default=False)
    is_active = models.BooleanField(verbose_name="Aktywny", default=True)

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
    class Meta:
        verbose_name = "Uzytkownik"
        verbose_name_plural = "Uzytkownicy"

    def __str__(self):
        return f"{self.username} mail: {self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class CarBrand(models.Model):
    brand_name = models.CharField(max_length=50, verbose_name="Marka", unique=True)

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Marki"

    def __str__(self):
        return f'{self.brand_name}'


class CarModel(models.Model):
    model_name = models.CharField(max_length=50, verbose_name="Model")
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Modele"

    def __str__(self):
        return f'{self.model_name}'


class Car(models.Model):
    plate_number = models.CharField(max_length=20, verbose_name="Numer rejestracyjny", unique=True)
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    year_of_production = models.IntegerField(verbose_name="Rok produkcji")
    rating = models.FloatField(verbose_name="Ocena")
    number_of_seats = models.IntegerField(verbose_name="Ilość miejsc")
    engine_type = models.CharField(max_length=20, verbose_name="Rodzaj silnika",
                                   choices=(('Benzynowy', 'Benzynowy'), ('Diesel', 'Diesel'), ('Elektryczny', 'Elektryczny'), ('Hybryda', 'Hybryda')))
    engine_power = models.IntegerField(verbose_name="Moc")
    color = models.CharField(max_length=50, verbose_name="Kolor")
    car_mileage = models.IntegerField(verbose_name="Przebieg")
    car_image = models.ImageField(upload_to='images/cars', verbose_name="Zdjęcie")
    gearbox_type = models.CharField(max_length=15, verbose_name="Skrzynia biegów", choices=(('Automatyczna', 'Automatyczna'), ('Manualna', 'Manualna')))

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"

    def __str__(self):
        return f'{self.plate_number} - {self.brand} {self.model}'
