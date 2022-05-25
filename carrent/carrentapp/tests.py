from django.test import TestCase, SimpleTestCase
from django.urls import reverse, reverse_lazy

from carrentapp.models import Car, CarBrand, CarModel


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
                                    year_of_production=12,
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
        # self.assertEqual(isinstance(self.car.brand, CarBrand), True)
        self.assertIsInstance(self.car.brand, CarBrand)
        self.assertEqual(self.car.year_of_production, 12)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/carrent/carlist/")
        self.assertEqual(response.status_code, 200)

    def test_car_list_page(self):
        response = self.client.get(reverse("car_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "carrentapp/car_list.html")
        self.assertContains(response, "<td>octavia</td>")