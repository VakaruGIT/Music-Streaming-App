from django.test import TestCase, Client
from django.urls import resolve

from .models import *
from .views import *
from .urls import *

# models.py

class TestUserModel(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_artist == False

    def test_user_password_hashing(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        assert user.password!= "password"  # password should be hashed

    def test_user_delete_cascade(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        user.delete()
        assert MusicTrack.objects.filter(id=music_track.id).exists() == False

class TestMusicTrackModel(TestCase):
    def test_music_track_creation(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        assert music_track.title == "Test Track"
        assert music_track.artist == user
        assert music_track.audio_file == "test.mp3"

    def test_music_track_delete_file(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        music_track.delete()
        assert default_storage.exists(music_track.audio_file.name) == False

class TestPlaylistModel(TestCase):
    def test_playlist_creation(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        assert playlist.name == "Test Playlist"
        assert playlist.user == user

    def test_playlist_add_track(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        playlist.tracks.add(music_track)
        assert playlist.tracks.count() == 1

    def test_playlist_remove_track(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        playlist.tracks.add(music_track)
        playlist.tracks.remove(music_track)
        assert playlist.tracks.count() == 0

# views.py

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        assert response.status_code == 200

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        assert response.status_code == 200

    def test_home_page_view(self):
        response = self.client.get(reverse("home-page"))
        assert response.status_code == 200

    def test_music_page_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("music_page"))
        assert response.status_code == 200

    def test_playlist_page_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        response = self.client.get(reverse("playlist_page", args=[playlist.id]))
        assert response.status_code == 200

    def test_upload_music_track_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        response = self.client.get(reverse("music_upload"))
        assert response.status_code == 200

    def test_edit_music_track_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        response = self.client.get(reverse("music_edit", args=[music_track.id]))
        assert response.status_code == 200

    def test_delete_music_track_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        music_track = MusicTrack.objects.create(title="Test Track", artist=user, audio_file="test.mp3")
        response = self.client.get(reverse("music_delete", args=[music_track.id]))
        assert response.status_code == 302  # redirect to music page

    def test_create_playlist_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        response = self.client.get(reverse("create_playlist"))
        assert response.status_code == 200

    def test_edit_playlist_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.client.login(username="testuser", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        response = self.client.post(reverse("edit_playlist", args=[playlist.id]),
                                    {"name": "Updated Playlist", "description": "Updated description"})
        assert response.status_code == 302 # redirect to playlist page

    def test_delete_playlist_view(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.client.login(username="testuser", password="password")
        playlist = Playlist.objects.create(name="Test Playlist", user=user)
        response = self.client.post(reverse("delete_playlist", args=[playlist.id]))
        assert response.status_code == 302  # redirect to playlists page

# urls.py
class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, login)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_home_page_url(self):
        url = reverse("home-page")
        self.assertEqual(resolve(url).func, home_page)

    def test_profile_url(self):
        url = reverse("profile")
        self.assertEqual(resolve(url).func, profile)

    def test_profile_edit_url(self):
        url = reverse("profile_edit")
        self.assertEqual(resolve(url).func, profile_edit)

    def test_edit_profile_redirect_url(self):
        url = reverse("edit_profile_redirect")
        self.assertEqual(resolve(url).func, edit_profile_redirect)

    def test_music_page_url(self):
        url = reverse("music_page")
        self.assertEqual(resolve(url).func, music_page)

    def test_music_upload_url(self):
        url = reverse("music_upload")
        self.assertEqual(resolve(url).func, upload_music_track)

    def test_music_edit_url(self):
        music_track_id = 1
        url = reverse("music_edit", args=[music_track_id])
        self.assertEqual(resolve(url).func, music_edit)

    def test_music_delete_url(self):
        music_track_id = 1
        url = reverse("music_delete", args=[music_track_id])
        self.assertEqual(resolve(url).func, music_delete)

    def test_music_search_url(self):
        url = reverse("music_search")
        self.assertEqual(resolve(url).func, music_search_page)

    def test_music_search_results_url(self):
        url = reverse("music_search_results")
        self.assertEqual(resolve(url).func, music_search_results)

    def test_playlists_page_url(self):
        url = reverse("playlists_page")
        self.assertEqual(resolve(url).func, playlists_page)

    def test_create_playlist_url(self):
        url = reverse("create_playlist")
        self.assertEqual(resolve(url).func, create_playlist)

    def test_playlist_page_url(self):
        playlist_id = 1
        url = reverse("playlist_page", args=[playlist_id])
        self.assertEqual(resolve(url).func, playlist_page)

    def test_delete_playlist_url(self):
        playlist_id = 1
        url = reverse("delete_playlist", args=[playlist_id])
        self.assertEqual(resolve(url).func, delete_playlist)

    def test_edit_playlist_url(self):
        playlist_id = 1
        url = reverse("edit_playlist", args=[playlist_id])
        self.assertEqual(resolve(url).func, edit_playlist)

    def test_add_to_playlist_url(self):
        song_id = 1
        url = reverse("add_to_playlist", args=[song_id])
        self.assertEqual(resolve(url).func, add_to_playlist)