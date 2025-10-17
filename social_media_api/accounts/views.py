# accounts/views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        user = request.user
        if target == user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if target in user.following.all():
            return Response({"detail": f"Already following {target.username}."}, status=status.HTTP_200_OK)

        user.following.add(target)
        return Response({"detail": f"Now following {target.username}."}, status=status.HTTP_200_OK)

class UnfollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        user = request.user
        if target == user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if target not in user.following.all():
            return Response({"detail": f"Not following {target.username}."}, status=status.HTTP_200_OK)

        user.following.remove(target)
        return Response({"detail": f"Unfollowed {target.username}."}, status=status.HTTP_200_OK)
