from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser
from model_mommy import mommy
from django.contrib.auth.hashers import check_password

# Create your tests here.


class TestCustomerRegister(APITestCase):

    def setUp(self):
        pass

    def test_customer_register(self):
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111111",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "7ujmnhy6"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)

    def test_customer_register_password_hash(self):
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111111",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "7ujmnhy6"
        }
        self.client.post(url, data=data)
        customer = CustomUser.objects.get(phone="09901111111")
        self.assertTrue(check_password("7ujmnhy6", customer.password))

    def test_customer_register_wrong_password(self):
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111111",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "111"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_customer_register_is_customer(self):
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111111",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "7ujmnhy6"
        }
        self.client.post(url, data=data)
        customer = CustomUser.objects.get(phone="09901111111")
        self.assertTrue(customer.is_customer)


class TestCustomerLogin(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser, phone='09901111112', password='7ujmnhy6')

    def test_customer_login_error(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111112",
            "password": "222"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)
