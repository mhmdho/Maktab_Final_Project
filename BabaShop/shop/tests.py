from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Product, Shop
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


class TestShopProducts(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop1 = mommy.make(Shop, supplier=self.user, name='darian',
                   type='hyper', is_confirmed=True)
        self.shop2 = mommy.make(Shop, supplier=self.user, name='plus',
                   type='organic', is_confirmed=True)
        self.shop3 = mommy.make(Shop, supplier=self.user, name='one',
                   type='supermarket', is_confirmed=False)
        self.product1 = mommy.make(Product, price=5, stock=5, shop=self.shop1, is_active=True)
        self.product2 = mommy.make(Product, price=15, stock=5, shop=self.shop1, is_active=True)
        self.product3 = mommy.make(Product, price=25, stock=5, shop=self.shop2, is_active=True)
        self.product4 = mommy.make(Product, price=35, stock=0, shop=self.shop2, is_active=True)
        self.product5 = mommy.make(Product, price=45, stock=5, shop=self.shop2, is_active=False)
        self.product6 = mommy.make(Product, price=55, stock=5, shop=self.shop3, is_active=False)

    def test_shop_product_list(self):
        url = reverse('shop_products_api', args=['darian_hyper'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_product_list_unauthorized(self):
        url = reverse('shop_products_api', args=['darian_hyper'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_product_count(self):
        url = reverse('shop_products_api', args=['darian_hyper'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)

    def test_shop_product_filter_tag(self):
        url = reverse('shop_products_api', args=['plus_organic'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'tag':3})
        self.assertEqual(resp.status_code, 200)

    def test_shop_product_filter_gt(self):
        url = reverse('shop_products_api', args=['plus_organic'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'price__gt':20})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 3)

    def test_shop_product_filter_lt(self):
        url = reverse('shop_products_api', args=['plus_organic'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'price__lt':30})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_shop_product_filter_is_active(self):
        url = reverse('shop_products_api', args=['plus_organic'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'available':True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
