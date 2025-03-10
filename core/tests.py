from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class PostAPITest(APITestCase):
    def setUp(self):
        # Создаем пользователя и пост для тестов
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, content="Test post content")
        self.client.force_authenticate(user=self.user)

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {
            'content': 'Updated post',
            'author': self.user.id  # Передаем автора, если требуется для PUT
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'), 'Updated post')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_likes_count_action(self):
        # Тестируем кастомное действие likes_count
        url = reverse('post-likes-count', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("likes", response.data)


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Аутентификация для доступа к UserViewSet
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        url = reverse('user-list')
        self.client.force_authenticate(user=self.user)  # Гарантируем аутентификацию
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, content="Test post for comment")
        self.comment = Comment.objects.create(author=self.user, post=self.post, content="Test comment")
        self.client.force_authenticate(user=self.user)

    def test_list_comments(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        data = {
            'content': 'Updated comment'
            # Для PATCH не нужно передавать поля, помеченные как read-only
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'), 'Updated comment')

    def test_delete_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LikeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, content="Post for like")
        self.like = Like.objects.create(user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)

    def test_list_likes(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_like(self):
        url = reverse('like-list')
        data = {
            'post': self.post.id,
            'user': self.user.id  # Передаем идентификатор пользователя
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
