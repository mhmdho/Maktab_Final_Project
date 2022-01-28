from rest_framework.test import APITestCase
from django.urls import reverse

from myuser.utils import OTP
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
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111112",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "7ujmnhy6"
        }
        self.client.post(url, data=data)

    def test_customer_login(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111112",
            "password": "7ujmnhy6"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_customer_login_password_error(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111112",
            "password": "222"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)
    
    def test_customer_login_phone_error(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111119",
            "password": "7ujmnhy6"
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)


class TestCustomerProfile(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser, phone='09901111112')

    def test_customer_profile_show(self):
        url = reverse('customer_profile_api')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_customer_profile_unauthorized(self):
        url = reverse('customer_profile_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

    def test_customer_profile_edit_error(self):
        url = reverse('customer_profile_api')
        self.client.force_authenticate(self.user)
        data = {
            "phone": "09901111111",
        }
        resp = self.client.put(url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_customer_profile_edit(self):
        url = reverse('customer_profile_api')
        self.client.force_authenticate(self.user)
        data = {
            "phone": "09901111111",
            "email": "mohammad@gmail.com",
            "username": "user111",
        }
        resp = self.client.put(url, data=data)
        self.assertEqual(resp.status_code, 200)


class TestCustomerPhoneVerify(APITestCase):

    def setUp(self):
        self.user1 = mommy.make(CustomUser,
                            phone='09901111114',
                            is_phone_verified=True)
        self.user2 = mommy.make(CustomUser,
                            phone='09901111115',
                            is_phone_verified=False)
    
    def test_customer_get_phone_has_verified_before(self):
        url = reverse('customer_phone_verify_api')
        self.client.force_authenticate(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    
    # def test_customer_phone_has_not_verified(self): # sending sms was ok
    #     url = reverse('customer_phone_verify_api')
    #     self.client.force_authenticate(self.user2)
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 201)

    def test_customer_put_phone_has_verified_before(self):
        url = reverse('customer_phone_verify_api')
        self.client.force_authenticate(self.user1)
        data = {
            "otp": "111111"
        }
        resp = self.client.put(url, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_customer_phone_verify_by_otp(self):
        url = reverse('customer_phone_verify_api')
        self.client.force_authenticate(self.user2)
        otp =OTP(self.user2.phone)
        # data = {
        #     "otp": "696220" #  verifying by sms was ok
        # }
        data = {
            "otp": otp.generate_token()
        }
        resp = self.client.put(url, data=data)
        self.assertEqual(resp.status_code, 202)
    
    def test_customer_phone_verify_wrong_otp(self):
        url = reverse('customer_phone_verify_api')
        self.client.force_authenticate(self.user2)
        data = {
            "otp": '222222'
        }
        resp = self.client.put(url, data=data)
        self.assertEqual(resp.status_code, 400)


class TestCustomerLoginOtp(APITestCase):

    def setUp(self):
        self.user1 = mommy.make(CustomUser,
                            phone='09901111114',
                            is_phone_verified=True)
        self.user2 = mommy.make(CustomUser,
                            phone='09901111115',
                            is_phone_verified=False)
    
    # def test_customer_login_otp_verified_phone(self): # sms sent
    #     url = reverse('supplier_login_otp_api')
    #     data = {
    #         "phone": self.user1.phone
    #     }
    #     resp = self.client.post(url, data=data)
    #     self.assertEqual(resp.status_code, 201)

    def test_customer_login_otp_not_verified_phone(self):
        url = reverse('supplier_login_otp_api')
        data = {
            "phone": self.user2.phone
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)

    def test_customer_login_otp_unregistered_phone(self):
        url = reverse('supplier_login_otp_api')
        data = {
            "phone": '09121111116'
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 404)


class TestCustomerLoginByOtp(APITestCase):

    def setUp(self):
        url = reverse('customer_register_api')
        data = {
            "phone": "09901111112",
            "email": "mohammad@gmail.com",
            "username": "user111",
            "password": "7ujmnhy6",
            "password2": "7ujmnhy6"
        }
        self.client.post(url, data=data)

    def test_customer_login_by_otp(self):
        url = reverse('token_obtain_pair')
        otp = OTP('09901111112')
        data = {
            "phone": "09901111112",
            "password": otp.generate_token()
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_customer_login_wrong_otp(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111112",
            "password": 'aa2222'
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)
    
    def test_customer_login_by_otp_phone_error(self):
        url = reverse('token_obtain_pair')
        otp = OTP('09901111112')
        data = {
            "phone": "09901111119",
            "password": otp.generate_token()
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 401)
    
    def test_customer_login_by_password(self):
        url = reverse('token_obtain_pair')
        data = {
            "phone": "09901111112",
            "password": '7ujmnhy6'
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
