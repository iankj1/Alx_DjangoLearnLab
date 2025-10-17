from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id", "actor", "actor_username", "verb", "timestamp",
            "read", "target_type", "target_object_id"
        ]
        read_only_fields = ["id", "actor", "actor_username", "verb", "timestamp", "target_type", "target_object_id"]

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
