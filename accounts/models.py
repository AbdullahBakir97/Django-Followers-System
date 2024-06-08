from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def follow(self, user_profile):
        if not self.is_following(user_profile):
            if user_profile.is_private:
                FollowRequest.objects.create(from_user=self, to_user=user_profile)
            else:
                Follower.objects.create(user=user_profile, follower=self)

    def unfollow(self, user_profile):
        Follower.objects.filter(user=user_profile, follower=self).delete()

    def is_following(self, user_profile):
        return Follower.objects.filter(user=user_profile, follower=self).exists()

    def has_follow_request(self, user_profile):
        return FollowRequest.objects.filter(from_user=self, to_user=user_profile).exists()

    def accept_follow_request(self, user_profile):
        follow_request = FollowRequest.objects.filter(from_user=user_profile, to_user=self).first()
        if follow_request:
            follow_request.accept()

    def reject_follow_request(self, user_profile):
        follow_request = FollowRequest.objects.filter(from_user=user_profile, to_user=self).first()
        if follow_request:
            follow_request.reject()

class Follower(models.Model):
    user = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.user}"

class FollowRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='follow_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='follow_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_user} wants to follow {self.to_user}"

    def accept(self):
        self.status = 'accepted'
        Follower.objects.create(user=self.to_user, follower=self.from_user)
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()