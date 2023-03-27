from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from films.api import serializers
from . import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform",
                                                           website="https://www.netflix.com")
        
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "The best streaming platform",
            "website": "https://www.netflix.com"
        }
        response = self.client.post(reverse('StreamPlatformVS-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_update(self):
        data = {
            "name": "Netflix updated streaming",
            "about": "The best streaming platform",
            "website": "https://www.netflix.com"
        }
        response = self.client.put(reverse('StreamPlatformVS-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('StreamPlatformVS-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('StreamPlatformVS-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('StreamPlatformVS-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform",
                                                           website="https://www.netflix.com")
        
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Eaxmple Movie",
                                                         storyline="Great Movie", active=True)
        
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "A great Movie",
            "active": True
        }
        response = self.client.post(reverse('movie_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_update(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie Updated",
            "storyline": "A great Movie again",
            "active": False
        }
        response = self.client.put(reverse('movie_detail', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie_detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Eaxmple Movie')
        
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('movie_detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform",
                                                           website="https://www.netflix.com")
        
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Eaxmple Movie",
                                                         storyline="Great Movie", active=True)
        
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Eaxmple Movie 2",
                                                         storyline="Awesome Movie", active=True)
        
        self.review = models.Review.objects.create(review_user=self.user, rating= 5,
                                                   description="what a powerful movie", watchlist=self.watchlist2,
                                                   active=True)
        
        
        
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "A great Movie",
            "watchlist": self.watchlist,
            "active" : True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.WatchList.objects.count(), 2)
    
    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "A great Movie",
            "watchlist": self.watchlist,
            "active" : True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "A great Movie Updated",
            "watchlist": self.watchlist,
            "active" : False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get('/movies/user-reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)