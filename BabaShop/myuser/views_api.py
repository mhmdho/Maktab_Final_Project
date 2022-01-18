from urllib import response
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
from datetime import timedelta, datetime
import time


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


OTP=TOTP(key=b'9fe43-4r54r-31034-rm32q', step=300, digits=6, t0=int(time.time()))

class CustomerPhoneVerify(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerPhoneVerifySerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def get(self, request, *args, **kwargs):     
        super().get(request, *args, **kwargs)
        expire = OTP.t0 + OTP.step * (OTP.t()+1)
        expire_at = datetime.fromtimestamp(expire).strftime('%Y-%b-%d %H:%M:%S')
        return Response({"Verify Code": str(OTP.token()).zfill(6),
                        "Expire at": expire_at},
                         status=status.HTTP_201_CREATED)
        
    def put(self, request, *args, **kwargs):
        try:
            token = int(self.request.data['otp'])
        except ValueError:
            self.verified = False
        else:
            if OTP.verify(token):
                self.verified = True
                customer = get_object_or_404(CustomUser, id=self.request.user.id)
                customer.is_phone_verified = True
                customer.save()
            else:
                self.verified = False
        super().put(request, *args, **kwargs)
        return Response({"Verified": self.verified}, status=status.HTTP_200_OK)
