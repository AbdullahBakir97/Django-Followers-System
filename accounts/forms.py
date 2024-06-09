from django import forms
from .models import User, FollowRequest, UserProfile
from django.core.exceptions import ValidationError

class FollowRequestForm(forms.ModelForm):
    class Meta:
        model = FollowRequest
        fields = []

    def save(self, commit=True):
        follow_request = super().save(commit=False)
        if commit:
            follow_request.save()
        return follow_request

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'is_private']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'image' ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'username': {
                'required': 'Username is required.',
                'unique': 'This username is already taken.',
            },
            'email': {
                'required': 'Email is required.',
                'invalid': 'Enter a valid email address.',
            },
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

class FollowRequestActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        self.follow_request = kwargs.pop('follow_request', None)
        super().__init__(*args, **kwargs)

    def clean_action(self):
        action = self.cleaned_data.get('action')
        if action not in ['accept', 'reject']:
            raise ValidationError("Invalid action.")
        return action

    def save(self):
        action = self.cleaned_data.get('action')
        if action == 'accept':
            self.follow_request.accept()
        elif action == 'reject':
            self.follow_request.reject()