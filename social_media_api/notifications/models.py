from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    """
    Simple notification model:
      - recipient: who receives the notification
      - actor: who performed the action
      - verb: short description e.g. "liked", "commented", "followed"
      - target: generic FK to the target object (post, comment, user, etc)
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actor_notifications"
    )
    verb = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    # generic target
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification({self.actor} {self.verb} -> {self.recipient})"
