from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Order, OrderItem, Product, Shop
from model_mommy import mommy

# Create your tests here.


class TestCreateOrder(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop = mommy.make(Shop, name='Darian', type='hyper', is_confirmed=True)
        self.order = mommy.make(Order, customer=self.user, shop=self.shop, is_payment=False)
        self.product1 = mommy.make(Product, id=101, price=20, stock=5, shop=self.shop, is_active=True, is_confirmed=True)
        self.product2 = mommy.make(Product, id=102, price=5, stock=1, shop=self.shop, is_active=False)
        self.product3 = mommy.make(Product, id=103, price=5, stock=1, is_active=True)

    def test_create_order_wrong_product(self):
        url = reverse('create_order_api', args=['darian_hyper'])
        self.client.force_authenticate(self.user)
        data = {
            "product": 103,
            "quantity": 2
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 404)

    def test_create_order_stock_error(self):
        url = reverse('create_order_api', args=['darian_hyper'])
        self.client.force_authenticate(self.user)
        data = {
            "product": 102,
            "quantity": 3
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_create_order_unauthorized(self):
        url = reverse('create_order_api', args=['darian_hyper'])
        data = {
            "product": 102,
            "quantity": 1
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)


class TestOrderItemList(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop = mommy.make(Shop, name='Darian', type='hyper', is_confirmed=True)
        self.order = mommy.make(Order, customer=self.user, shop=self.shop, is_payment=False)

    def test_orderitem_list(self):
        url = reverse('create_order_api', args=['darian_hyper'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_orderitem_list_unauthorized(self):
        url = reverse('create_order_api', args=['darian_hyper'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)


class TestOrderItemDelete(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop = mommy.make(Shop, name='Darian', type='hyper', is_confirmed=True)
        self.order = mommy.make(Order, customer=self.user, shop=self.shop, is_payment=False)
        self.product1 = mommy.make(Product, id=101, price=20, stock=5, shop=self.shop, is_active=True, is_confirmed=True)
        self.orderitem = mommy.make(OrderItem, order=self.order, id=1, product=self.product1, quantity=2)

    def test_orderitem_delete(self):
        url = reverse('delete_order_api', kwargs={"slug":"darian_hyper","pk": 1})
        self.client.force_authenticate(self.user)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)

    def test_orderitem_delete_unauthorized(self):
        url = reverse('delete_order_api', kwargs={"slug":"darian_hyper","pk": 1})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 401)

    def test_orderitem_delete(self):
        url = reverse('delete_order_api', kwargs={"slug":"darian_hyper","pk": 1})
        self.client.force_authenticate(self.user)
        self.client.delete(url)
        self.assertEqual(self.product1.stock, 3)#

    def test_orderitem_delete_wrong(self):
        url = reverse('delete_order_api', kwargs={"slug":"darian_hyper","pk": 2})
        self.client.force_authenticate(self.user)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 404)


class TestPayOrderPay(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.shop = mommy.make(Shop, name='Darian', type='hyper', is_confirmed=True)
        self.order = mommy.make(Order, id=1, customer=self.user, shop=self.shop, is_payment=False)
        self.product1 = mommy.make(Product, id=101, price=20, stock=5, shop=self.shop, is_active=True, is_confirmed=True)
        self.orderitem = mommy.make(OrderItem, order=self.order, id=1, product=self.product1, quantity=2)

    def test_pay_order(self):
        url = reverse('pay_order_api', kwargs={"slug":"darian_hyper","pk": 1})
        self.client.force_authenticate(self.user)
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, 202)

    def test_pay_order_unauthorized(self):
        url = reverse('pay_order_api', kwargs={"slug":"darian_hyper","pk": 1})
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, 401)

    def test_pay_order_wrong(self):
        url = reverse('pay_order_api', kwargs={"slug":"darian_hyper","pk": 2})
        self.client.force_authenticate(self.user)
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, 400)


class TestOpenOrders(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.order = mommy.make(Order, is_payment=False, customer=self.user)
        self.order = mommy.make(Order, is_payment=True, customer=self.user)

    def test_open_order_list(self):
        url = reverse('open_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_open_order_unauthorized(self):
        url = reverse('open_order_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def test_open_order_is_payment(self):
        url = reverse('open_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 1)


class TestClosedOrders(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser)
        self.order = mommy.make(Order, is_payment=False, customer=self.user)
        self.order = mommy.make(Order, is_payment=True, customer=self.user, _quantity=3)

    def test_closed_order_list(self):
        url = reverse('closed_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    
    def test_closed_order_unauthorized(self):
        url = reverse('closed_order_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def test_closed_order_is_payment(self):
        url = reverse('closed_order_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 3)
