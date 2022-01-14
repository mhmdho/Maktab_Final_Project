from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Product, Shop
from model_mommy import mommy

# Create your tests here.


class TestCreateOrder(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop = mommy.make(Shop, name='Darian', type='hyper', is_confirmed=True)
        self.product1 = mommy.make(Product, id=101, price=20, stock=5, shop=self.shop, is_active=True)
        self.product2 = mommy.make(Product, id=102, price=5, stock=1, shop=self.shop, is_active=True)


    def test_create_order(self):
        url = reverse('create_order_api', args=['Darian_hyper'])
        self.client.force_authenticate(self.user)
        data = {
            "product": 101
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 404)#

    def test_create_order_error(self):
        url = reverse('create_order_api', args=['Darian_hyper'])
        self.client.force_authenticate(self.user)
        data = {
            "product": 102,
            "quantity": 2
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 404)#


class TestOrderItemList(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)

    def test_orderitem_list(self):
        url = reverse('create_order_api', args=['Darian_hyper'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)#


class TestOpenOrders(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)

    def test_open_order_list(self):
        url = reverse('open_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_open_order_unauthorized(self):
        url = reverse('open_order_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

class TestClosedOrders(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)

    def test_open_order_list(self):
        url = reverse('closed_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    
    def test_open_order_unauthorized(self):
        url = reverse('closed_order_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
