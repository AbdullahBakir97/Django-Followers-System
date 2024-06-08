from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OnlineUser, UserProfile, Follower, FollowRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'userId')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('userId',)
    
@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_private', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_private', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower', 'created_at')
    search_fields = ('user__user__username', 'follower__user__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at', 'updated_at')
    search_fields = ('from_user__user__username', 'to_user__user__username')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        for follow_request in queryset:
            follow_request.accept()
        self.message_user(request, "Selected follow requests have been accepted.")
    accept_requests.short_description = "Accept selected follow requests"

    def reject_requests(self, request, queryset):
        for follow_request in queryset:
            follow_request.reject()
        self.message_user(request, "Selected follow requests have been rejected.")
    reject_requests.short_description = "Reject selected follow requests"