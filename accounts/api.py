from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from .models import User, UserProfile, FollowRequest, Follower
from .serializers import UserProfileSerializer, FollowRequestSerializer, FollowerSerializer, UserSerializer, LoginSerializer, SignupSerializer
from django.shortcuts import get_object_or_404

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

class SendFollowRequest(generics.CreateAPIView):
    serializer_class = FollowRequestSerializer
    queryset = FollowRequest.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_user_ids = request.data.get('user_ids', [])
        from_user = request.user.userprofile
        responses = []

        print(f"Initial count of following: {from_user.following.count()}")

        for user_id in to_user_ids:
            to_user = get_object_or_404(UserProfile.objects.prefetch_related('user'), id=user_id)
            if from_user.has_follow_request(to_user) or from_user.is_following(to_user):
                responses.append({'user_id': user_id, 'detail': 'You have already sent a follow request or are already following this user.'})
                continue

            follow_request = FollowRequest(from_user=from_user, to_user=to_user)
            follow_request.save()
            responses.append(FollowRequestSerializer(follow_request).data)

        print(f"Response data: {responses}")
        print(f"Number of follow requests: {len(responses)}")
        print(f"Final count of following: {from_user.following.count()}")

        return Response(responses, status=status.HTTP_201_CREATED)
    
    
class HandleFollowRequest(generics.UpdateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    # permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        follow_request = get_object_or_404(FollowRequest, id=self.kwargs['request_id'])
        if follow_request.to_user != request.user.userprofile:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get('action')
        if action == 'accept':
            follow_request.accept()
        elif action == 'reject':
            follow_request.reject()
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FollowRequestSerializer(follow_request).data)

class UnfollowUser(generics.DestroyAPIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(UserProfile, id=self.kwargs['user_id'])
        request.user.userprofile.unfollow(user_to_unfollow)
        return Response({'detail': 'You have unfollowed this user.'}, status=status.HTTP_204_NO_CONTENT)

class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, id=self.kwargs['user_id'])

class APIRootView(views.APIView):
    def get(self, request, *args, **kwargs):
        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id

        return Response({
            'profile': reverse('api_profile_detail', request=request),
            'user_profile': reverse('api_user_profile', kwargs={'user_id': user_id}, request=request),  # Example user_id
            'send_follow_request': reverse('api_send_follow_request', request=request),
            'unfollow_user': reverse('api_unfollow_user', kwargs={'user_id': user_id}, request=request),  # Example user_id
            'handle_follow_request': reverse('api_handle_follow_request', kwargs={'request_id': user_id}, request=request),  # Example request_id
            'user_list': reverse('user_list', request=request),
            'login': reverse('login', request=request),
            'signup': reverse('signup', request=request),
            'chat_rooms': reverse('chat_rooms', request=request),
            'chat_messages': reverse('chat_messages', kwargs={'roomId': 'example_room_id'}, request=request),  # Example roomId
        })
        
        
    
    
class UserView(ListAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        excludeUsersArr = []
        try:
            excludeUsers = self.request.query_params.get('exclude')
            if excludeUsers:
                userIds = excludeUsers.split(',')
                for userId in userIds:
                    excludeUsersArr.append(int(userId))
        except:
            return []
        return super().get_queryset().exclude(id__in=excludeUsersArr)

class LoginApiView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

class SignupApiView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer