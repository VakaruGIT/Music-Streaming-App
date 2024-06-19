from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, get_user_model
from django.contrib.auth.views import LogoutView
from django.urls import reverse

# Create your views here.
def register(request): # DONE
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = False
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home-page")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout(request): # DONE
    return LogoutView.as_view(request)

def home_page(request): # DONE
    music_tracks = MusicTrack.objects.all()
    return render(request, "home-page.html", {"music_tracks": music_tracks})

def profile(request):
    user = request.user
    return render(request, "user_profile.html", {"user": user})

def profile_edit(request):
    user = get_user_model().objects.get(username=request.user.username)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to profile view
    else:
        form = UserUpdateForm(instance=user, initial={
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "bio": user.bio,
        })
    return render(request, "user_profile_edit.html", {"form": form, "user": user})

def edit_profile_redirect(request):
    return redirect("profile_edit")


def upload_music_track(request): # DONE
    if request.method == "POST":
        form = MusicTrackForm(request.POST, request.FILES)
        if form.is_valid():
            music_track = form.save(commit=False)
            music_track.artist = request.user
            music_track.save()
            return redirect("music_page")
    else:
        form = MusicTrackForm()
    return render(request, "music_upload.html", {"form": form})

def music_page(request):
    music_tracks = MusicTrack.objects.all()
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "music_page.html", {"music_tracks": music_tracks, "playlists": playlists})


def music_edit(request, music_track_id): # DONE
    music_track = MusicTrack.objects.get(id=music_track_id)
    if request.method == "POST":
        form = MusicTrackForm(request.POST, request.FILES, instance=music_track)
        if form.is_valid():
            form.save()
            return redirect("music_page")
    else:
        form = MusicTrackForm(instance=music_track)
    return render(request, "music_edit.html", {"form": form, "music_track": music_track})

def music_delete(request, music_track_id): # DONE
    music_track = MusicTrack.objects.get(id=music_track_id)
    music_track.delete()
    return redirect("music_page")

def music_search_page(request): # DONE
    return render(request, "music_search.html")

def music_search_results(request): # DONE
    song_name = request.GET.get("song_name")
    artist_name = request.GET.get("artist_name")
    genre = request.GET.get("genre")

    songs = MusicTrack.objects.all()

    if song_name:
        songs = songs.filter(title__icontains=song_name)
    if artist_name:
        songs = songs.filter(artist__name__icontains=artist_name)
    if genre:
        songs = songs.filter(genre__icontains=genre)

    return render(request, "music_search_results.html", {"songs": songs})

def playlists_page(request):
    user = request.user
    playlists = Playlist.objects.filter(user=user).order_by("-id")
    return render(request, "playlists_page.html", {"playlists": playlists})

def playlist_page(request, playlist_id):
    current_playlist = Playlist.objects.get(id=playlist_id)
    tracks = current_playlist.tracks.all()
    return render(request, "playlist_page.html", {"current_playlist": current_playlist, "tracks": tracks})

def create_playlist(request):
    if request.method == "POST":
        name = request.POST["name"]
        tracks = request.POST.getlist("tracks")

        playlist = Playlist.objects.create(name=name, user=request.user)

        for track_id in tracks:
            add_to_playlist(request, playlist.id, track_id)

        return redirect("playlist_page", playlist_id=playlist.id)

    music_tracks = MusicTrack.objects.all()
    return render(request, "create_playlist.html", {"music_tracks": music_tracks})

def edit_playlist(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    if request.method == "POST":
        form = PlaylistUpdateForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            tracks = request.POST.getlist("tracks")
            playlist.tracks.clear()
            for track_id in tracks:
                track = MusicTrack.objects.get(id=track_id)
                playlist.tracks.add(track)
            return redirect("playlist_page", playlist_id=playlist.id)
    else:
        form = PlaylistUpdateForm(instance=playlist)
        tracks = MusicTrack.objects.all()
        playlist_tracks = playlist.tracks.all()
    return render(request, "edit_playlist.html", {"form": form, "playlist": playlist, "tracks": tracks, "playlist_tracks": playlist_tracks})

def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id)
    track = MusicTrack.objects.get(id=song_id)

    playlist.tracks.remove(track)
    return redirect("playlist_page", playlist_id=playlist_id)

def add_to_playlist(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id)
    track = MusicTrack.objects.get(id=song_id)

    playlist.tracks.add(track)
    return redirect("playlist_page", playlist_id=playlist_id)

def delete_playlist(request, playlist_id):
    try:
        playlist_id = int(playlist_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()
        return redirect(reverse("playlists_page"))
    except ValueError:
        return redirect(reverse("playlists_page"))
    except Playlist.DoesNotExist:
        return redirect(reverse("playlists_page"))

