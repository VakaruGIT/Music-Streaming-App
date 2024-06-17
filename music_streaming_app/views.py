from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages

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

# def update_profile(request): #DONE
#     user = get_user_model().objects.get(username=request.user.username)
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = UserUpdateForm(instance=user)
#     return render(request, 'user_profile.html', {'form': form})

def upload_music_track(request): # DONE
    if request.method == 'POST':
        form = MusicTrackForm(request.POST, request.FILES)
        if form.is_valid():
            music_track = form.save(commit=False)
            music_track.artist = request.user
            music_track.save()
            messages.success(request, 'Music track uploaded successfully!')
            return redirect('music_page')
    else:
        form = MusicTrackForm()
    return render(request, 'music_upload.html', {'form': form})

def music_page(request): # DONE
    music_tracks = MusicTrack.objects.all()
    return render(request, 'music_page.html', {'music_tracks': music_tracks})


def music_edit(request, music_track_id):
    music_track = MusicTrack.objects.get(id=music_track_id)
    if request.method == 'POST':
        form = MusicTrackForm(request.POST, request.FILES, instance=music_track)
        if form.is_valid():
            form.save()
            return redirect('music_page')
    else:
        form = MusicTrackForm(instance=music_track)
    return render(request, 'music_edit.html', {'form': form, 'usic_track': music_track})

def music_delete(request, music_track_id):
    music_track = MusicTrack.objects.get(id=music_track_id)
    music_track.delete()
    return redirect('music_page')

def music_search_page(request):
    return render(request, 'music_search.html')

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
        songs = songs.filter(genre__icontains=genre)

    if not songs:
        messages.info(request, 'No music found with this information.')

    return render(request, 'music_search_results.html', {'songs': songs})



