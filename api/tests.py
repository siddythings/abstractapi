from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import User
from .models import Post

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@gmail.com')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, content='Test post content')

    def test_create_post(self):
        url = reverse('create-post')
        data = {'content': 'New post content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_post(self):
        url = reverse('post-detail', kwargs={'post_id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test post content')

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'post_id': self.post.id})
        data = {'content': 'Updated post content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated post content')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'post_id': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        url = reverse('like-post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.post.likes.all())

    def test_unlike_post(self):
        self.post.likes.add(self.user)
        url = reverse('unlike-post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user, self.post.likes.all())
