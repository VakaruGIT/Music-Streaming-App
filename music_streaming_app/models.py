from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
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
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio_files/')
    genre = models.CharField(max_length=50)

