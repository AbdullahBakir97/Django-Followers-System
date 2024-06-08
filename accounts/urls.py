from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.send_follow_request, name='send_follow_request'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('follow-request/<int:request_id>/', views.handle_follow_request, name='handle_follow_request'),
    path('api/', api.APIRootView.as_view(), name='api_root'),
    path('api/profile/', api.UserProfileDetail.as_view(), name='api_profile_detail'),
    path('api/profile/<int:user_id>/', api.UserProfileView.as_view(), name='api_user_profile'),
    path('api/follow/', api.SendFollowRequest.as_view(), name='api_send_follow_request'),
    path('api/unfollow/<int:user_id>/', api.UnfollowUser.as_view(), name='api_unfollow_user'),
    path('api/follow-request/<int:request_id>/', api.HandleFollowRequest.as_view(), name='api_handle_follow_request'),
]
