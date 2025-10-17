# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import PostViewSet, CommentViewSet, FeedListAPIView, LikeAPIView, UnlikeAPIView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedListAPIView.as_view(), name="feed"),
    path("posts/<int:pk>/like/", LikeAPIView.as_view(), name="post-like"),
    path("posts/<int:pk>/unlike/", UnlikeAPIView.as_view(), name="post-unlike"),
]
