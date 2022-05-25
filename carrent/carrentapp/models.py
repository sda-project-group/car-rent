from datetime import date

from django.db import models

from accounts.models import UserCustom


class CarBrand(models.Model):
    brand_name = models.CharField(max_length=50, verbose_name="Marka", unique=True)

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Marki"

    def __str__(self):
        return f'{self.brand_name}'


class CarModel(models.Model):
    model_name = models.CharField(max_length=50, verbose_name="Model")
    brand = models.ForeignKey(CarBrand, verbose_name="Marka", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Modele"

    def __str__(self):
        return f'{self.model_name}'


class Car(models.Model):
    plate_number = models.CharField(max_length=20, verbose_name="Numer rejestracyjny", unique=True)
    brand = models.ForeignKey(CarBrand, verbose_name="Marka", on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModel, verbose_name="Model", on_delete=models.PROTECT)

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
        return f'{self.plate_number} - {self.brand} {self.car_model}'


class BasePrice(models.Model):
    base_price = models.IntegerField(verbose_name="Cena Bazowa")

    class Meta:
        verbose_name = "Cena Bazowa"
        verbose_name_plural = "Cena Bazowa"

    def __str__(self):
        return f'Cena Bazowa: {self.base_price}'


class Order(models.Model):
    client = models.ForeignKey(UserCustom, verbose_name="Klient", on_delete=models.PROTECT)
    car = models.ForeignKey(Car, verbose_name="Samochód", on_delete=models.PROTECT)
    base_price = models.ForeignKey(BasePrice, verbose_name="Cena bazowa", on_delete=models.PROTECT)

    rent_cost = models.IntegerField(verbose_name="Koszt wynajmu", blank=True, null=True)
    start_date = models.DateField(verbose_name="Start")
    return_date = models.DateField(verbose_name="Zwrot")
    order_datetime = models.DateTimeField(verbose_name="Powstanie zamówienia", auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Edytowane", auto_now=True)

    status = models.CharField(max_length=10,
                              verbose_name="Status",
                              choices=(
                                  ('Aktywny', 'Aktywny'),
                                  ('Historia', 'Historia')),
                              default='Aktywny')

    class Meta:
        verbose_name = "Log Wypozyczenia"
        verbose_name_plural = "Logi Wypozyczen"

    def __str__(self):
        return f'{self.client.email} {self.car.plate_number} =>ID {self.id}'

    @property
    def cost_calculator(self):
        nr_of_days = self.return_date - self.start_date
        price_per_day = self.base_price.base_price * self.car.rating
        return nr_of_days.days * price_per_day

    @property
    def is_future(self):
        if self.start_date > date.today():
            return True
        else:
            return False

    @property
    def is_past(self):
        if self.return_date < date.today():
            return True
        else:
            return False

    def save(self, *args, **kwarg):
        self.rent_cost = self.cost_calculator
        super(Order, self).save(*args, **kwarg)
