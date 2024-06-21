from django.urls import path
from. import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    #  REGISTER, LOGIN, LOGOUT
    path("", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", LogoutView.as_view(next_page ="register"), name="logout"),

    # HOME PAGE
    path("home/", views.home_page, name="home-page"),

    # PROFILE
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/edit_redirect/", views.edit_profile_redirect, name="edit_profile_redirect"),

    # MUSIC
    path("music/", views.music_page, name="music_page"),
    path("music/upload/", views.upload_music_track, name="music_upload"),
    path("music/edit/<int:music_track_id>/", views.music_edit, name="music_edit"),
    path("music/delete/<int:music_track_id>/", views.music_delete, name="music_delete"),
    path("music/search/", views.music_search_page, name="music_search"),
    path("music/search/results/", views.music_search_results, name="music_search_results"),

    # PLAYLIST
    path("playlists/", views.playlists_page, name="playlists_page"),
    path("playlists/create/", views.create_playlist, name="create_playlist"),
    path("playlists/<int:playlist_id>/", views.playlist_page, name="playlist_page"),
    path("playlists/<int:playlist_id>/delete/", views.delete_playlist, name="delete_playlist"),
    path("playlists/<int:playlist_id>/edit/", views.edit_playlist, name="edit_playlist"),
    path("add_to_playlist/<int:song_id>/", views.add_to_playlist, name="add_to_playlist"),
]