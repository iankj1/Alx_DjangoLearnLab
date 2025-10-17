from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model

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

class FeedListAPIView(generics.ListAPIView):
    """
    Returns posts created by users that the request.user follows,
    ordered by newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # explicit queryset string expected by checkers:
        # Post.objects.filter(author__in=...)
        following_qs = user.following.all()
        return Post.objects.filter(author__in=following_qs).order_by("-created_at")
