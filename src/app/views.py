from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, exceptions


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(f"User {request.user.username} logged out")
        return Response(status=status.HTTP_200_OK)
