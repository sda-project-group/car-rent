import datetime
from datetime import datetime
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from carrentapp.models import Car, CarBrand, CarModel, Order, BasePrice


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/carrent/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse_lazy('main'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, "carrentapp/home_page.html")

    def test_template_content(self):
        response = self.client.get(reverse('main'))
        self.assertContains(response, "<h3>Jakość</h3>")
        self.assertNotContains(response, "Not on the page")


class CarListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.carbrand = CarBrand.objects.create(brand_name='Skoda')
        cls.carmodel = CarModel.objects.create(model_name="octavia",
                                               brand=cls.carbrand)
        cls.car = Car.objects.create(plate_number='DOA 553',
                                     brand=cls.carbrand,
                                     car_model=cls.carmodel,
                                     year_of_production=2012,
                                     rating=0.5,
                                     number_of_seats=5,
                                     engine_type='Elektryczny',
                                     engine_power=200,
                                     color='red',
                                     car_mileage='10000',
                                     car_image='C:\SDA\projekt\car-rent\carrent\carrentapp\static\carrentapp\images\main-carousel-1.jpg',
                                     gearbox_type='Automatyczna')

    def test_model_content(self):
        self.assertEqual(self.car.plate_number, 'DOA 553')
        self.assertEqual(self.car.brand.brand_name, 'Skoda')
        self.assertEqual(isinstance(self.car.brand, CarBrand), True)
        self.assertIsInstance(self.car.brand, CarBrand)
        self.assertEqual(self.car.year_of_production, 2012)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/carrent/carlist")
        self.assertEqual(response.status_code, 200)

    def test_car_list_page(self):
        response = self.client.get(reverse("car_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "carrentapp/car_list.html")
        self.assertContains(response, "<td>octavia</td>")


class OrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.baseprice = BasePrice.objects.create(base_price=100)
        cls.client = get_user_model().objects.create(email='malgorzata.pilch12@gmail.com',
                                                     username='gosia',
                                                     first_name='gosia',
                                                     last_name='pilch',
                                                     birthdate='1999-01-01',
                                                     addr_city='szczecin',
                                                     addr_street='gdanska',
                                                     addr_post_code='32-700',
                                                     mobile_nr='600123123')
        cls.carbrand = CarBrand.objects.create(brand_name='Skoda')
        cls.carmodel = CarModel.objects.create(model_name="octavia",
                                               brand=cls.carbrand)
        cls.car = Car.objects.create(plate_number='DOA 553',
                                     brand=cls.carbrand,
                                     car_model=cls.carmodel,
                                     year_of_production=2012,
                                     rating=0.5,
                                     number_of_seats=5,
                                     engine_type='Elektryczny',
                                     engine_power=200,
                                     color='red',
                                     car_mileage='10000',
                                     car_image='C:\SDA\projekt\car-rent\carrent\carrentapp\static\carrentapp\images\main-carousel-1.jpg',
                                     gearbox_type='Automatyczna')

        cls.order = Order.objects.create(client=cls.client,
                                         car=cls.car,
                                         base_price=cls.baseprice,
                                         rent_cost=100,
                                         start_date=datetime.strptime("2022-06-02", '%Y-%m-%d').date(),
                                         return_date=datetime.strptime("2022-06-04", '%Y-%m-%d').date(),
                                         status='Aktywny')

    def test_model_content(self):
        self.assertEqual(self.order.rent_cost, 100)
        self.assertEqual(self.baseprice.base_price, 100)
        self.assertEqual(self.order.status, 'Aktywny')

    def test_cost_rent_a_car_per_day(self):
        price_per_day = self.baseprice.base_price * self.car.rating
        self.assertEqual(price_per_day, 50)

    def test_cost_calculator(self):
        rent_days = self.order.return_date - self.order.start_date
        number_of_days = int(rent_days.days)
        self.assertEqual(number_of_days, 2)

