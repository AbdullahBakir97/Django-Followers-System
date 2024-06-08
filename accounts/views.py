from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, FollowRequest, Follower
from .forms import FollowRequestForm, FollowRequestActionForm, UserProfileForm, UserForm

@login_required
def send_follow_request(request, user_id):
    to_user = get_object_or_404(UserProfile, id=user_id)
    from_user = request.user.userprofile

    if from_user.has_follow_request(to_user) or from_user.is_following(to_user):
        messages.error(request, 'You have already sent a follow request or are already following this user.')
        return redirect('profile', user_id=to_user.id)
    
    if request.method == 'POST':
        form = FollowRequestForm(request.POST)
        if form.is_valid():
            follow_request = form.save(commit=False)
            follow_request.from_user = from_user
            follow_request.to_user = to_user
            follow_request.save()
            messages.success(request, 'Follow request sent successfully.')
            return redirect('profile', user_id=to_user.id)
    else:
        form = FollowRequestForm()

    return render(request, 'accounts/send_follow_request.html', {'form': form, 'to_user': to_user})

@login_required
def handle_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id)
    if follow_request.to_user != request.user.userprofile:
        messages.error(request, 'Invalid request.')
        return redirect('profile', user_id=request.user.userprofile.id)

    if request.method == 'POST':
        form = FollowRequestActionForm(request.POST, follow_request=follow_request)
        if form.is_valid():
            form.save()
            messages.success(request, f'Follow request {form.cleaned_data["action"]}ed.')
            return redirect('profile', user_id=follow_request.to_user.id)
    else:
        form = FollowRequestActionForm(follow_request=follow_request)

    return render(request, 'accounts/handle_follow_request.html', {'form': form, 'follow_request': follow_request})

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(UserProfile, id=user_id)
    request.user.userprofile.unfollow(user_to_unfollow)
    messages.success(request, 'You have unfollowed this user.')
    return redirect('profile', user_id=user_to_unfollow.id)

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', user_id=user_profile.id)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    is_following = request.user.userprofile.is_following(user_profile)
    has_follow_request = request.user.userprofile.has_follow_request(user_profile)
    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'is_following': is_following,
        'has_follow_request': has_follow_request
    })