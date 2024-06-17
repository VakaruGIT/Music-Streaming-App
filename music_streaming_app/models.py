from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from pydub import AudioSegment
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    is_artist = models.BooleanField(default=False)
    email = models.EmailField(blank=True)

    def set_password(self, password):
        self.password = make_password(password)

    def __str__(self):
        return self.username


class MusicTrack(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    audio_file = models.FileField(upload_to='audio_files/')
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} by {self.artist.name} ({self.genre})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the audio file from the media folder
        default_storage.delete(self.audio_file.name)
        super().delete(*args, **kwargs)