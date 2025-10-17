# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_profile_picture_path(instance, filename):
    return f"profile_pictures/user_{instance.id}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path, blank=True, null=True
    )
    # Users this user follows
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True
    )

    def __str__(self):
        return self.username
