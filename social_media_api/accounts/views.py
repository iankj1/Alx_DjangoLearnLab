# accounts/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={"request": request}).data
        return Response({"token": token.key, "user": user_data}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "user": UserSerializer(user, context={"request": request}).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "username"  # profile accessible by /profile/<username>/

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

class FollowToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        user = request.user
        if user == target:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        if user in target.followers.all():
            target.followers.remove(user)
            action = "unfollowed"
        else:
            target.followers.add(user)
            action = "followed"

        return Response({"detail": f"{action} {target.username}."}, status=200)
