import time
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import UserProfile
from .serializers import SignUpSerializer, SignSerializer


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({"msg": 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    permission_classes = [permissions.AllowAny]
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = SignSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.get_authenticated_user(serializer.validated_data)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        return Response({
            'id': user.username,
            'type_id': user_profile.id_type,
        })


class Latency(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        start = time.time()
        try:
            requests.get('https://ya.ru', timeout=5)
        except requests.RequestException:
            return Response({'latency': 'Error getting ya.ru'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        end = time.time()
        return Response({'latency': f'{(end - start) * 1000:.2f} ms'})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        all_tokens = request.data.get('all', False)
        if all_tokens:
            for token in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.get_or_create(token=token)
            return Response({'detail': 'All tokens invalidated'}, status=status.HTTP_200_OK)
        else:
            raw_token = request.META.get('HTTP_AUTHORIZATION', None)
            if raw_token:
                prefix, _, token_str = raw_token.partition(' ')
                try:
                    token_obj = RefreshToken(token_str)
                    token_obj.blacklist()
                except Exception:
                    pass
            return Response({'detail': 'Current token invalidated'}, status=status.HTTP_200_OK)
