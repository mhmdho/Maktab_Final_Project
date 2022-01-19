from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from myuser.models import CustomUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerPhoneVerifySerializer, CustomerProfileSerializer, RegisterSerializer
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase, serializers
from rest_framework.parsers import FormParser, MultiPartParser

from django_otp.oath import TOTP
from django_otp.util import random_hex
from datetime import datetime
import time
from django.core.cache import cache


# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    parser_classes = (MultiPartParser, FormParser)


class TokenRefreshView2(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = serializers.TokenRefreshSerializer
    parser_classes = (MultiPartParser, FormParser)

token_refresh = TokenRefreshView2.as_view()


class CustomerRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"Success": "Your registration was successful"}, status=status.HTTP_201_CREATED)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    http_method_names = ['put', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class CustomerPhoneVerify(generics.RetrieveUpdateAPIView):
    http_method_names = ['put', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerPhoneVerifySerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def get(self, request, *args, **kwargs):   
        super().get(request, *args, **kwargs)
        customer = get_object_or_404(CustomUser, id=self.request.user.id)
        if customer.is_phone_verified:
            return Response({"Message": "Your phone have been verified"},
                            status=status.HTTP_200_OK)
        OTP=TOTP(key=bytes(random_hex(), 'utf-8'), 
                step=300, digits=6, t0=int(time.time()))
        expire = OTP.t0 + OTP.step * (OTP.t()+1)
        expire_at = datetime.fromtimestamp(expire).strftime('%Y-%b-%d %H:%M:%S')
        cache.set(customer.phone, OTP.token(), timeout=300)
        return Response({"Verify Code": OTP.token(),
                        "Expire at": expire_at},
                         status=status.HTTP_201_CREATED)
        
    def put(self, request, *args, **kwargs):
        customer = get_object_or_404(CustomUser, id=self.request.user.id)
        if customer.is_phone_verified:
            return Response({"Message": "Your phone have been verified before"},
                            status=status.HTTP_200_OK)
        try:
            entered_otp = int(self.request.data['otp'])
        except ValueError:
            pass
        else:
            otp = cache.get(customer.phone)
            if otp == entered_otp:
                customer.is_phone_verified = True
                customer.save()

        super().put(request, *args, **kwargs)
        return Response({"Verified": customer.is_phone_verified},
                        status=status.HTTP_200_OK)
