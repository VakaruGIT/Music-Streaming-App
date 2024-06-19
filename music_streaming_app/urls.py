from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # LOGIN, REGISTER, LOGOUT
    path('', views.register, name='register'), # DONE
    path('login/', views.login, name='login'), # DONE
    path('logout/', LogoutView.as_view(next_page ="register"), name='logout'), # DONE
    # HOME PAGE
    path("home/", views.home_page, name="home-page"), # DONE
    # PROFILE
    path("profile/", views.profile, name="profile"), # DONE
    path('profile/edit/', views.profile_edit, name='profile_edit'), # DONE
    path('profile/edit_redirect/', views.edit_profile_redirect, name='edit_profile_redirect'), # DONE
    # MUSIC
    path("music/", views.music_page, name="music_page"), # DONE
    path('music/upload/', views.upload_music_track, name='music_upload'), # DONE
    path('music/edit/<int:music_track_id>/', views.music_edit, name='music_edit'), # DONE
    path('music/delete/<int:music_track_id>/', views.music_delete, name='music_delete'), # DONE
    path('music/search/', views.music_search_page, name='music_search'), # DONE
    path("music/search/results/", views.music_search_results, name="music_search_results"), # DONE
    # PLAYLIST
    path("playlists/", views.playlists_page, name="playlists_page"),  # DONE
    path("playlists/create/", views.create_playlist, name="create_playlist"),  # DONE
    path("playlists/<int:playlist_id>/", views.playlist_page, name="playlist_page"),  # DONE
    path("playlists/<int:playlist_id>/edit/", views.edit_playlist, name="playlist_edit"),  # DONE
    path("playlists/<int:playlist_id>/delete/", views.delete_playlist, name="playlist_delete"),  # DONE
    path("add_to_playlist/<int:song_id>/", views.add_to_playlist, name="add_to_playlist"),  # DONE
]