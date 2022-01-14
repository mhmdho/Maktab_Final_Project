from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Shop
from model_mommy import mommy

# Create your tests here.


class TestShopConfirmedList(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        mommy.make(Shop, supplier=self.user,
                   type='hyper', is_confirmed=True)
        mommy.make(Shop, supplier=self.user,
                   type='organic', is_confirmed=True)
        mommy.make(Shop, supplier=self.user,
                   type='supermarket', is_confirmed=False)


    def test_shop_confirmed_show(self):
        url = reverse('shop_confirmed_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_confirmed_unauthorized(self):
        url = reverse('shop_confirmed_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_confirmed_count(self):
        url = reverse('shop_confirmed_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)
    
    def test_shop_confirmed_filter_null(self):
        url = reverse('shop_confirmed_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'type': 'supermarket'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 0)

    def test_shop_confirmed_filter(self):
        url = reverse('shop_confirmed_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'type': 'organic'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)


class TestShoptypes(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        mommy.make(Shop, supplier=self.user,
                   type='hyper', is_confirmed=True)
        mommy.make(Shop, supplier=self.user,
                   type='organic', is_confirmed=True)
        mommy.make(Shop, supplier=self.user,
                   type='supermarket', is_confirmed=False)

    def test_shop_types(self):
        url = reverse('shop_types_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_types_unauthorized(self):
        url = reverse('shop_types_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_types_count(self):
        url = reverse('shop_types_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)