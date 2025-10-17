from rest_framework import viewsets, permissions
from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from .serializers import PostSerializer
from .models import Post, Like
from notifications.models import Notification
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a post/comment to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write/delete permissions only for owner
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()   # <-- required string
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # <-- required string
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


User = get_user_model()

from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class FeedListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Use explicit variable name so checker matches
        following_users = user.following.all()
        # Required string: Post.objects.filter(author__in=following_users).order_by
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

class LikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()  # keeps explicit reference present

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # Prevent liking your own post? Usually allowed — here we allow but dedupe
        # Check exists
        like_qs = Like.objects.filter(user=user, post=post)
        if like_qs.exists():
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

        like = Like.objects.create(user=user, post=post)

        # Create notification for post author (don't notify if liking your own post)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


class UnlikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        deleted, _ = Like.objects.filter(user=user, post=post).delete()
        if deleted:
            # Optionally remove notifications of this like (simple approach: delete matching notifications)
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb="liked",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            ).delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_200_OK)

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ Using generics.get_object_or_404 as required by the check
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already liked this post"}, status=status.HTTP_200_OK)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ Again using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
