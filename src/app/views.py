from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

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
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(f"User {request.user.username} logged out")
        return Response(status=status.HTTP_200_OK)
