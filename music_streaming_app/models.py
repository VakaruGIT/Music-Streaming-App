from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage

class User(AbstractUser):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField()
    is_artist = models.BooleanField(default=False)
    email = models.EmailField(blank=True)

    def set_password(self, password): # Hash password
        self.password = make_password(password)

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs): # Delete all tracks by artist when artist is deleted
        if self.is_artist:
            MusicTrack.objects.filter(artist=self).delete()
        super().delete(*args, **kwargs)


class MusicTrack(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    audio_file = models.FileField(upload_to='audio_files/')
    genre = models.CharField(max_length=50)

    def __str__(self): # Return track title, artist name, and genre
        return f"{self.title} by {self.artist.name} ({self.genre})"

    def delete(self, *args, **kwargs): # Delete audio file when track is deleted
        default_storage.delete(self.audio_file.name)
        super().delete(*args, **kwargs)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(MusicTrack, related_name='playlists')

    def __str__(self): # Return playlist name and user name
        return f"{self.name} by {self.user.name}"

    def add_track(self, track): # Add track to playlist
        self.tracks.add(track)
        self.save()

    def remove_track(self, track): # Remove track from playlist
        self.tracks.remove(track)
        self.save()

    def clear(self): # Clear all tracks from playlist
        self.tracks.clear()
        self.save()

    def delete(self, *args, **kwargs): # Clear all tracks from playlist when playlist is deleted
        self.tracks.clear()
        super().delete(*args, **kwargs)