# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")

class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source="author", required=False
    )
    post_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Post.objects.all(), source="post"
    )

    class Meta:
        model = Comment
        fields = ("id", "post", "post_id", "author", "author_id", "content", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at", "post")

    def create(self, validated_data):
        # 'author' should come from view (request.user) — but support author_id if provided
        author = self.context["request"].user
        post = validated_data.pop("post")
        return Comment.objects.create(author=author, post=post, **validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "created_at", "updated_at", "comments_count", "comments")
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments_count", "comments")

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        # author will be assigned in the view (request.user) — keep create minimal
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)
