from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,MusicTrack
from django.contrib.auth.models import Group

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'bio', 'profile_picture', 'is_artist')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        if user.is_artist:
            artist_group, created = Group.objects.get_or_create(name='Artist')
            user.groups.add(artist_group)
        else:
            user_group, created = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("name", "bio", "profile_picture","email")




class MusicTrackForm(forms.ModelForm):
    class Meta:
        model = MusicTrack
        fields = ("title","artist","genre","audio_file")