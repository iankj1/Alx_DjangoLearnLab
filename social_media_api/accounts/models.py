from django.db import models
from django.contrib.auth.models import AbstractUser  # <-- required import

def user_profile_picture_path(instance, filename):
    return f"profile_pictures/user_{instance.id}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # <-- models.TextField
    profile_picture = models.ImageField(           # <-- models.ImageField
        upload_to=user_profile_picture_path,
        blank=True,
        null=True
    )
    followers = models.ManyToManyField(            # <-- models.ManyToManyField
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )

    def __str__(self):
        return self.username
