from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import UserProfile, FollowRequest, Follower
from rest_framework import status
import logging

class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        self.client.login(username='user1', password='password')

    def test_send_follow_request(self):
        # Ensure user1 is following no one initially
        print("Initial count of following:", self.user1.userprofile.following.count())

        # Prepare data for sending follow request to user2 and user3
        data = {'user_ids': [self.user2.userprofile.id, self.user3.userprofile.id]}

        # Make POST request to send follow request
        response = self.client.post('/accounts/api/follow/', data, format='json')

        # Log the response status code and data
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if follow requests were created for user2 and user3
        follow_requests = FollowRequest.objects.filter(from_user=self.user1.userprofile)
        print("Number of follow requests:", follow_requests.count())

        # Check if user1 is now following user2 and user3
        print("Final count of following:", self.user1.userprofile.following.count())

        # Check the response data structure
        for follow_request in response.data:
            self.assertIn('from_user', follow_request)
            self.assertIn('to_user', follow_request)
            self.assertIn('status', follow_request)

    def test_unfollow_user(self):
        self.user1.userprofile.follow(self.user2.userprofile)
        response = self.client.delete(f'/accounts/api/unfollow/{self.user2.userprofile.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_profile(self):
        data = {
            'user': {
                'username': 'newuser1',
                'email': 'newuser1@example.com',
                'first_name': 'New',
                'last_name': 'User1'
            },
            'bio': 'New bio',
            'is_private': True
        }
        response = self.client.put('/accounts/api/profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'newuser1')
        self.assertEqual(self.user1.userprofile.bio, 'New bio')
        self.assertTrue(self.user1.userprofile.is_private)

    def test_accept_follow_request(self):
        self.client.logout()
        self.client.login(username='user2', password='password')
        follow_request = FollowRequest.objects.create(from_user=self.user1.userprofile, to_user=self.user2.userprofile)
        data = {'action': 'accept'}
        response = self.client.put(f'/accounts/api/follow-request/{follow_request.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'accepted')
        self.assertTrue(Follower.objects.filter(user=self.user2.userprofile, follower=self.user1.userprofile).exists())

    def test_reject_follow_request(self):
        self.client.logout()
        self.client.login(username='user2', password='password')
        follow_request = FollowRequest.objects.create(from_user=self.user1.userprofile, to_user=self.user2.userprofile)
        data = {'action': 'reject'}
        response = self.client.put(f'/accounts/api/follow-request/{follow_request.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'rejected')
        self.assertFalse(Follower.objects.filter(user=self.user2.userprofile, follower=self.user1.userprofile).exists())