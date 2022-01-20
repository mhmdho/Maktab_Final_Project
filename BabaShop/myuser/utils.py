from django_otp.oath import TOTP
from datetime import datetime
import time


class OTP:
    """
    Generate otp based on user phone number.
    """
    def __init__(self, phone):        
        self.digits = 6
        self.step = 300  # seconds that otp will expire
        self.key = bytes(phone+str(time.time()//self.step), 'utf-8')
        self.last_verified_counter = -1
        self.verified = False

    def totp_obj(self):
        totp = TOTP(key=self.key, step=self.step, digits=self.digits)
        return totp

    def generate_token(self):
        return str(self.totp_obj().token()).zfill(6)

    def verify_token(self, token, tolerance=0):
        try:
            token = int(token)
        except ValueError:
            self.verified = False
        else:
            totp = self.totp_obj()

            if ((totp.t() > self.last_verified_counter) and
                    (totp.verify(token, tolerance=tolerance))):
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                self.verified = False
        return self.verified
    
    @property
    def expire_at(self):
        totp = self.totp_obj()
        expire = totp.t0 + totp.step * (totp.t()+1)
        return datetime.fromtimestamp(expire).strftime('%Y-%b-%d %H:%M:%S')
