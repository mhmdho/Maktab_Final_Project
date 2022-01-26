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
        "Code": otp,
        "MobileNumber": phone
        })
    headers = {
        'Content-Type': 'application/json',
        'x-sms-ir-secure-token': response.json()["TokenKey"]
        }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


@shared_task
def kavenegar_otp(phone, otp):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API)
        params = {
            'sender' : settings.KAVENEGAR_SENDER,
            'receptor': phone,
            'message' : f'Code: {otp.generate_token()} -\
                        Expire: {otp.expire_at}'
                }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print('1---------',e)
    except HTTPException as e:
        print('2---------',e)
