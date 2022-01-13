from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser
from model_mommy import mommy

# Create your tests here.


class TestShopConfirmedList(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)

    def test_shop_confirmed_show(self):
        url = reverse('shop_confirmed_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_confirmed_unauthorized(self):
        url = reverse('shop_confirmed_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)