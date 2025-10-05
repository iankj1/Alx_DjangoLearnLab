from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        # users
        self.author = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')

        # a post
        self.post = Post.objects.create(author=self.author, title='Test', content='Content')

        # login client for author
        self.client.login(username='author', password='pass')

    def test_create_comment_authenticated(self):
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        response = self.client.post(url, {'content': 'A new comment'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.comments.filter(content='A new comment').exists())

    def test_create_comment_unauthenticated_redirects(self):
        from django.test import Client
        client = Client()
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        response = client.post(url, {'content': 'nope'})
        # LoginRequiredMixin redirects to login by default (302)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.post.comments.filter(content='nope').exists())

    def test_update_comment_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.author, content='Initial')
        url = reverse('comment-update', kwargs={'pk': comment.pk})
        response = self.client.post(url, {'content': 'Edited'}, follow=True)
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited')

    def test_update_comment_by_other_forbidden(self):
        comment = Comment.objects.create(post=self.post, author=self.author, content='Initial')
        # log in as other user
        self.client.logout()
        self.client.login(username='other', password='pass')
        url = reverse('comment-update', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        # raises 403 since raise_exception=True
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.author, content='To delete')
        url = reverse('comment-delete', kwargs={'pk': comment.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
