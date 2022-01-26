from inspect import Parameter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from myuser.models import CustomUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerLoginOtpSerializer, CustomerPhoneVerifySerializer, CustomerProfileSerializer, RegisterSerializer
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase, serializers
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from .utils import OTP
from myuser.tasks import smsir_otp


# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
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
    """
    Takes a set of informations and register customer.
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"Success": "Your registration was successful"}, status=status.HTTP_201_CREATED)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """
    Shows and update the customer profile.
    """
    http_method_names = ['put', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class CustomerPhoneVerify(generics.RetrieveUpdateAPIView):
    """
    Generates an otp and takes the otp to verify customer phone number.
    """
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
        otp = OTP(customer.phone)
        # cache.set(customer.phone, otp.generate_token(), timeout=300)
        return Response({"Verify Code": otp.generate_token(),
                        "Expire at": otp.expire_at},
                         status=status.HTTP_201_CREATED)
        
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
        customer = get_object_or_404(CustomUser, id=self.request.user.id)
        if customer.is_phone_verified:
            return Response({"Message": "Your phone have been verified before"},
                            status=status.HTTP_200_OK)
        otp = OTP(customer.phone)
        if otp.verify_token(self.request.data['otp']):
            customer.is_phone_verified = True
            customer.save()
            return Response({"Verified": customer.is_phone_verified},
                            status=status.HTTP_200_OK)
        return Response({"Error": "Wrong OTP or expired"},
                        status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginOtp(generics.GenericAPIView):
    """
    Generates otp in order to customer login.
    Customer can also login with phone and otp.
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomerLoginOtpSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        responses={'201': 'Return otp + expirataion time',
                   '401': 'If user phone not verified',
                   '404': 'If user not registered'}
    )
    def post(self, request, *args, **kwargs):
        customer = CustomUser.objects.filter(
            phone=self.request.data['phone']).first()
        if customer:
            if customer.is_phone_verified:
                otp = OTP(self.request.data['phone'])
                smsir_otp.delay('09353666110', otp.generate_token())
                return Response({"Verify Code": otp.generate_token(),
                                "Expire at": otp.expire_at},
                                    status=status.HTTP_201_CREATED)
            return Response({"Error": "Your phone is not verified"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({"Error": "You have not registered yet"},
                        status=status.HTTP_404_NOT_FOUND)
                        