from django.test import TestCase
from carrentapp.models import Order, BasePrice, Car, CarBrand, CarModel
from django.test import Client


class TestModels(TestCase):

    def test_model_str_brand_name(self):
        brand_name = CarBrand.objects.create(brand_name="Volvo")
        self.assertEqual(str(brand_name), "Volvo")