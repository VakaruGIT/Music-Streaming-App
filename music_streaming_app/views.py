from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

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

def login(request): # DONE
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home-page")
            else:
                return render(request, "login.html", {"form": form, "error": "Invalid username or password"})
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout(request): # DONE
    return LogoutView.as_view(request)

def home_page(request): # DONE
    music_tracks = MusicTrack.objects.all()
    return render(request, "home-page.html", {"music_tracks": music_tracks})

@login_required
def profile(request): # DONE
    user = get_user_model().objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user_profile.html', {'form': form})

@login_required
def update_profile(request): #DONE
    user = get_user_model().objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user_profile.html', {'form': form})

@login_required
def music_upload(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = MusicTrackForm(request.POST, request.FILES)
            if form.is_valid():
                music_track = form.save(commit=False)
                music_track.artist = request.user
                music_track.save()
                return redirect("home-page")
            else:
                return HttpResponse("Invalid form")
        else:
            return HttpResponse("You must be logged in to upload music")
    else:
        if request.user.is_authenticated:
            form = MusicTrackForm()
            return render(request, "music_upload.html", {"form": form})
        else:
            return HttpResponse("You must be logged in to upload music")

def music_page(request):
    music_tracks = MusicTrack.objects.all()
    return render(request, "music_page.html", {"music_tracks": music_tracks})


def music_search_results(request):
    song_name = request.GET.get('song_name')
    artist_name = request.GET.get('artist_name')
    genre = request.GET.get('genre')

    songs = MusicTrack.objects.all()

    if song_name:
        songs = songs.filter(title__icontains=song_name)
    if artist_name:
        songs = songs.filter(artist__name__icontains=artist_name)
    if genre:
        songs = songs.filter(genre__name__icontains=genre)

    return render(request, 'music_search_results.html', {'songs': songs})


# def music_play(request, music_track_id):
#     music_track = MusicTrack.objects.get(id=music_track_id)
#     audio_file = music_track.audio_file
#     return HttpResponse(audio_file, content_type="audio/mpeg")

