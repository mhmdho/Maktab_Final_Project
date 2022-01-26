from django.conf import settings
import requests
import json
from celery import shared_task
from kavenegar import *


@shared_task
def smsir_otp(phone, otp):

    url = "https://RestfulSms.com/api/Token"
    payload = json.dumps({
        "UserApiKey": settings.SMSIR_SECRET_CODE,
        "SecretKey": settings.SMSIR_API_KEY
        })
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data=payload)


    url = "https://RestfulSms.com/api/VerificationCode"
    payload = json.dumps({
        "Code": "12345",
        "MobileNumber": "09353666110"
        })
    headers = {
        'Content-Type': 'application/json',
        'x-sms-ir-secure-token': response.json()["TokenKey"]
        }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
