from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

class Post(models.Model):
    """
    Blog post model.
    - author: FK to User (one user can have many posts).
    - title, content: user-editable.
    - created_at, updated_at: timestamps.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # used by generic CreateView/UpdateView redirect on success
        return reverse('post-detail', kwargs={'pk': self.pk})

class Profile(models.Model):
    """
    Extends the built-in User model with optional fields.
    Kept minimal: bio and avatar (profile picture path).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile: {self.user.username}'

# Signal to create or save profile automatically when user is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        
class Comment(models.Model):
    """
    Comment left by a User on a Post.
    - post: FK to Post (many comments per post).
    - author: FK to User (the commenter).
    - content: text of the comment.
    - created_at / updated_at: timestamps.
    """
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # oldest first for readability

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_absolute_url(self):
        # After creating / editing / deleting a comment we usually return to the post detail
        return reverse('post-detail', kwargs={'pk': self.post.pk})
